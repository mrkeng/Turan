from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturalday
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from tagging.fields import TagField
import types
from os.path import join

from photos.models import Pool, Image

from celery.task.sets import subtask
from datetime import datetime

from durationfield import DurationField

from gpxparser import GPXParser, proj_distance

from tcxwriter import TCXWriter

from tasks import create_simplified_gpx, create_svg_from_gpx, create_gpx_from_details, \
        merge_sensordata, calculate_ascent_descent_gaussian, calculate_best_efforts, \
        parse_sensordata

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

gpxstore = FileSystemStorage(location=settings.GPX_STORAGE)

class RouteManager(models.Manager):
    ''' Primary purpose to remove the /dev/null route. Will also hide "one time routes" '''

    def get_query_set(self):
        # TODO, this needs to be a fixture, with a fixed ID
        return super(RouteManager, self).get_query_set().exclude(pk=24)#.filter(single_serving=0)


class Route(models.Model):
    name = models.CharField(max_length=160, blank=True, help_text=_('for example Opsangervatnet'))
    distance = models.FloatField(help_text=_('in km'), default=0)
    description = models.TextField(help_text=_('route description'))
    route_url = models.URLField(blank=True) # gmaps?
    gpx_file = models.FileField(upload_to='gpx', blank=True, storage=gpxstore)
    ascent = models.IntegerField(blank=True, null=True) # m
    descent = models.IntegerField(blank=True, null=True) # m

    start_lat = models.FloatField(blank=True, default=0.0)
    start_lon = models.FloatField(blank=True, default=0.0)
    end_lat = models.FloatField(blank=True, default=0.0)
    end_lon = models.FloatField(blank=True, default=0.0)

    created = models.DateTimeField(editable=False,auto_now_add=True,null=True)
    single_serving = models.BooleanField(blank=True, default=0)

    tags = TagField()

    objects = RouteManager()

    def save(self, force_insert=False, force_update=False):
        # If we have gpx file set but not start_lat set, parse gpx and set start and end positions
        if self.gpx_file:
            if not self.start_lat or not self.distance or not self.ascent:
                    g = GPXParser(self.gpx_file.file)
                    if g:
                        # set coordinates for route if it doesn't exist
                        if not self.start_lat:
                            self.start_lon = g.start_lon
                            self.start_lat = g.start_lat
                            self.end_lon = g.end_lon
                            self.end_lat = g.end_lat
                        if not self.distance:
                            # distance calculated in meters in parser
                            self.distance = g.distance/1000.0
                        if not self.ascent:
                            self.ascent = g.ascent
                            self.descent = g.descent
        super(Route, self).save(force_insert, force_update)
        if self.gpx_file:
            # generate svg if it doesn't exist (after save, it uses id for filename)
            filename = 'svg/%s.svg' %self.id
            if not gpxstore.exists(filename):
                create_svg_from_gpx.delay(self.gpx_file.path, filename)

            # generate simplified gpx to use as layer, for faster loading
            filename = 'gpx/%s.simpler.gpx' %self.id
            if not gpxstore.exists(filename):
                create_simplified_gpx.delay(self.gpx_file.path, filename)

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return ("Unnamed trip")

    def get_simplegpx_url(self):
        url = None
        if self.gpx_file:
            filename = 'gpx/%s.simpler.gpx' %self.id
            if gpxstore.exists(filename):
                url = filename
                #//url = '/'.join(self.gpx_file.url.split('/')[0:-2]) + '/' + filename
            else:
                url = self.gpx_file
        return url

    def get_absolute_url(self):
        if not self.single_serving:
            return reverse('route', kwargs={ 'object_id': self.id }) + '/' + slugify(self.name)

    def get_svg_url(self):
        if self.gpx_file:
            filename = 'svg/%s.svg' %self.id
            #return gpxstore.url(filename) Broken ?
            return '%sturan/%s' %(settings.MEDIA_URL, filename)
        else:
            return ''

    class Meta:
        verbose_name = _("Route")
        verbose_name_plural = _("Routes")
        ordering = ('-created','name')

    def get_trips(self):
        return self.exercise_set.all().order_by('duration')

    def get_photos(self):
        ct = ContentType.objects.get_for_model(self)
        return [pool.photo for pool in Pool.objects.filter(content_type=ct, object_id=self.id)]

    def add_photo(self, photo):
        p = Pool(content_object=self, image=photo)
        p.save()

    @property
    def tripcount(self):
        ''' used in triplist, nice for sorting '''
        return len(self.get_trips())

    def get_geo_title(self):
        lon1, lat1 = self.start_lon, self.start_lat
        lon2, lat2 = self.end_lon, self.end_lat
        if lon1 and lat1 and lat2 and lon2:
            s_distance = 99999999
            farthest_lon, farthest_lat = self.find_farthest_pos_from_start()
            f_distance = 99999999
            e_distance = 99999999
            start_town = ''
            farthest_town = ''
            end_town = ''

            for loc in Location.objects.all():
                this_distance = proj_distance(lat1, lon1, loc.lat, loc.lon)
                if this_distance < s_distance:
                    start_town = loc.town
                    s_distance = this_distance
                if farthest_lon and farthest_lat:
                    this_distance = proj_distance(farthest_lat, farthest_lon, loc.lat, loc.lon)
                    if this_distance < f_distance:
                        farthest_town = loc.town
                        f_distance = this_distance
                this_distance = proj_distance(lat2, lon2, loc.lat, loc.lon)
                if this_distance < e_distance:
                    end_town = loc.town
                    e_distance = this_distance
            if farthest_town:
                if start_town == end_town and farthest_town != end_town:
                    return '%s %s %s' %(start_town, farthest_town, end_town)
                if start_town != farthest_town != end_town:
                    return '%s %s %s' %(start_town, farthest_town, end_town)
                if start_town == farthest_town == end_town:
                    return start_town
                elif start_town == farthest_town:
                    return '%s %s' %(start_town, end_town)
                elif end_town == farthest_town:
                    return '%s %s' %(start_town, end_town)
                if start_town == end_town:
                    return start_town
            else:
                if start_town == end_town:
                    return start_town
                return '%s %s' %(start_town, end_town)

    def find_farthest_pos_from_start(self):
        if self.gpx_file:
            details = GPXParser(self.gpx_file).entries
            if details:
                lon, lat = details[0].lon, details[0].lat
                distance = 0
                max_lon, max_lat = 0, 0
                for d in details:
                    this_lon, this_lat = d.lon, d.lat
                    if this_lon and this_lat:
                        this_distance = proj_distance(lat, lon, this_lat, this_lon)
                        if this_distance > distance:
                            distance = this_distance
                            max_lon, max_lat = this_lon, this_lat
                return max_lon, max_lat


class ExerciseManager(models.Manager):
    ''' Some permission related purposes '''

    def get_query_set(self):
        return super(ExerciseManager, self).get_query_set().exclude(exercise_permission='N')

    #def get_by_userteams(self, user_id):
    #    innerq = TeamMembership.objects.filter(user=user_id).values('team').query
    #    return self.filter(user__team__in=innerq)

    #def get_by_teamname(self, teamname):
    #    return self.filter(user__team__name__exact=teamname)
#class Team(models.Model):
#    name = models.CharField(max_length=160, help_text=_('Team name'))
#    description = models.TextField(help_text=_('info'))
#    slogan = models.TextField(blank=True, help_text=_('No pain - no gain'))
#    logo = models.ImageField(upload_to='team_logos', blank=True, storage=gpxstore)
#    url = models.URLField(blank=True)
#
#    members = models.ManyToManyField(User, through='TeamMembership')
#
#    def get_absolute_url(self):
#        return reverse('team', kwargs={ 'object_id': self.id }) + '/' + slugify(self.name)
#
#    def __unicode__(self):
#        return self.name
#
#    class Meta:
#        verbose_name = _("Team")
#        verbose_name_plural = _("Teams")
#        ordering = ('name',)
#
#class TeamMembership(models.Model):
#    user = models.ForeignKey(User)
#    team = models.ForeignKey(Team)
#    date_joined = models.DateField()
#    role = models.CharField(max_length=64, help_text=_('i.e. Captain'))
#
#    class Meta:
#        verbose_name = _("Team Membership")
#        verbose_name_plural = _("Team Memberships")
class ExerciseType(models.Model):

    name = models.CharField(max_length=40)
    logo = models.ImageField(upload_to='exerciselogos', blank=True, storage=gpxstore)
    altitude = models.BooleanField(blank=True, default=0)
    slopes = models.BooleanField(blank=True, default=0)

    def __unicode__(self):
        return ugettext(self.name)

    def __repr__(self):
        return unicode(self.name)

    def icon(self):
        # FIXME use media url
        if self.logo:
            return settings.MEDIA_URL + 'turan/%s' %(self.logo)
        return ''


    class Meta:
        verbose_name = _("Exercise Type")
        verbose_name_plural = _("Exercise Types")
        ordering = ('name',)

permission_choices = (
            ('A', 'All'),
            ('F', 'Friends'),
            ('N', 'None'),
                    )

class Exercise(models.Model):

    user = models.ForeignKey(User)
    exercise_type = models.ForeignKey(ExerciseType, default=13) # FIXME hardcoded to cycling
    route = models.ForeignKey(Route, blank=True, null=True, help_text=_("Search existing routes"))
    duration = DurationField(blank=True, default=0, help_text='18h 30m 23s 10ms 150mis')
    date = models.DateField(blank=True, null=True, help_text=_("year-mo-dy"))
    time = models.TimeField(blank=True, null=True, help_text="00:00:00")

    comment = models.TextField(blank=True)
    url = models.URLField(blank=True)

    avg_speed = models.FloatField(blank=True, null=True) #kmt
    avg_cadence = models.IntegerField(blank=True, null=True) # rpm
    avg_pedaling_cad = models.IntegerField(blank=True, null=True) # rpm
    avg_power = models.IntegerField(blank=True, null=True) # W
    avg_pedaling_power = models.IntegerField(blank=True, null=True) # W

    max_speed = models.FloatField(blank=True, null=True) #kmt
    max_cadence = models.IntegerField(blank=True, null=True) # rpm
    max_power = models.IntegerField(blank=True, null=True) # W

    avg_hr = models.IntegerField(blank=True, null=True) # bpm 
    max_hr = models.IntegerField(blank=True, null=True) # bpm 

    kcal = models.IntegerField(blank=True, default=0, help_text=_('Only needed for Polar products'))

    temperature = models.FloatField(blank=True, null=True, help_text=_('Celsius'))
    sensor_file = models.FileField(upload_to='sensor', blank=True, storage=gpxstore, help_text=_('File from equipment from Garmin/Polar (.gpx, .tcx, .hrm, .gmd, .csv)'))

    exercise_permission = models.CharField(max_length=1, choices=permission_choices, default='A', help_text=_('Visibility choice'))

    object_id = models.IntegerField(null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    group = generic.GenericForeignKey("object_id", "content_type")

    tags = TagField(help_text='f.eks. sol regn uhell punktering')

    #objects = models.Manager() # default manager

    #testm = CycleTripManager()
#    objects = ExerciseManager()

    def get_details(self):
        return self.exercisedetail_set

    def save(self, *args, **kwargs):
        super(Exercise, self).save(*args, **kwargs)
        if self.sensor_file:
            if not self.route and str(self.exercise_type) == "Cycling":
                r = Route()
                r.name = str(self.user) + " " + datetime.now().strftime('%d%m%y')
                r.description = "Autoroute"
                r.single_serving = True
                r.save()
                self.route = r
        # set avg_speed if distance and duration is given
        if self.route and self.route.distance and self.duration and not self.avg_speed:
            self.avg_speed = float(self.route.distance)/(float(self.duration.seconds)/60/60)

        super(Exercise, self).save(*args, **kwargs)

    def parse(self):
        #task = parse_sensordata.delay(self)
        #print task
        if self.sensor_file:
            task = parse_sensordata.delay(self)
#, callback=subtask(merge_sensordata, callback=subtask(calculate_best_efforts)))
#, 
#                    callback=subtask(create_gpx_from_details,
#                    callback=subtask(calculate_best_efforts
#                    ))))
            return task
        return None


    def get_absolute_url(self):
        route_name = ''
        if self.route:
            route_name = slugify(self.route.name)
        return reverse('exercise', kwargs={ 'object_id': self.id }) + '/' + route_name

    def get_geojson_url(self):
        return reverse('geojson', kwargs={'object_id': self.id})

    def get_simplegpx_url(self):
        ''' Also defined here in addition to in Route because of how Mapper.js is initiated '''
        if self.route:
            return self.route.get_simplegpx_url()


    def icon(self):
        return self.exercise_type.icon()

    def is_smart_sampled(self):
        filename = self.sensor_file.name
        if filename.lower().endswith('.tcx'):
            exercise_details = self.get_details().all()[1:3]
            delta_t = (exercise_details[1].time - exercise_details[0].time).seconds
            if delta_t > 1:
                return True
        return False

    class Meta:
        verbose_name = _("Exercise")
        verbose_name_plural = _("Exercises")
        ordering = ('-date','-time')

    def __unicode__(self):
        name = _('Unnamed trip')
        if self.route and self.route.name:
            name = self.route.name
# FIXME 
            if name == '/dev/null':
                name = unicode(self.exercise_type)
        else:
            name = unicode(self.exercise_type)

        return u'%s, %s %s' %(name, _('by'), self.user)

    def delete(self, *args, **kwargs):
        ''' Also delete single serving route '''
        if self.route:
            if self.route.single_serving:
                r = self.route
                r.delete()
        super(Exercise, self).delete(*args, **kwargs)


class ExercisePermission(models.Model):
    exercise = models.OneToOneField(Exercise, primary_key=True)
    speed = models.CharField(max_length=1, choices=permission_choices, default='A')
    power = models.CharField(max_length=1, choices=permission_choices, default='A')
    cadence = models.CharField(max_length=1, choices=permission_choices, default='A')
    hr = models.CharField(max_length=1, choices=permission_choices, default='A')

class ExerciseDetail(models.Model):

    exercise = models.ForeignKey(Exercise)
    time = models.DateTimeField()
    speed = models.FloatField(blank=True, null=True)
    hr = models.IntegerField(blank=True, null=True)
    altitude = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    cadence = models.IntegerField(blank=True, null=True)
    power = models.IntegerField(blank=True, null=True)

    def get_relative_time(self):
        start_time = datetime(self.time.year, self.time.month, self.time.day, self.trip.time.hour, self.trip.time.minute, self.trip.time.second)
        return self.time - start_time

    class Meta:
        ordering = ('time',)


class BestPowerEffort(models.Model):
    exercise = models.ForeignKey(Exercise)
    pos = models.FloatField()
    length = models.FloatField()
    duration = models.IntegerField()
    power = models.IntegerField()
    ascent = models.IntegerField()
    descent = models.IntegerField()

    class Meta:
        ordering = ('duration',)

class BestSpeedEffort(models.Model):
    exercise = models.ForeignKey(Exercise)
    pos = models.FloatField()
    length = models.FloatField()
    duration = models.IntegerField()
    speed = models.FloatField()
    ascent = models.IntegerField()
    descent = models.IntegerField()

    class Meta:
        ordering = ('duration',)

merge_choices = (
            ('M', _('Merge')),
            ('P', _('Prepend')),
            ('A', _('Append')),
                    )

class MergeSensorFile(models.Model):
    exercise = models.ForeignKey(Exercise)
    merge_strategy = models.CharField(max_length=1, choices=merge_choices, default='M', help_text=_('Merge strategy. Merge = Merge on top of current, Append = Append to end, Prepend = Insert before current'))
    sensor_file = models.FileField(upload_to='sensor', storage=gpxstore, help_text=_('File from equipment from Garmin/Polar (.gpx, .tcx, .hrm, .gmd, .csv, .pwx, .xml)'))
    hr = models.BooleanField(blank=True, default=0)
    power = models.BooleanField(blank=True, default=0)
    cadence = models.BooleanField(blank=True, default=0)
    altitude = models.BooleanField(blank=True, default=0)
    position = models.BooleanField(blank=True, default=0)
    speed = models.BooleanField(blank=True, default=0)

    def save(self, *args, **kwargs):
        ''' Trigger merging on creation '''
        super(MergeSensorFile, self).save(*args, **kwargs)
        merge_sensordata.apply(self.exercise)

    def __unicode__(self):
        result = 'Merge type %s with types: ' % self.merge_strategy
        vals = []
        for val in ('hr', 'power', 'cadence', 'altitude', 'speed', 'position'):
            if getattr(self, val):
                vals.append(val)
        result += ','.join(vals)
        result += u', into %s' % self.exercise

        return result

class Slope(models.Model):
    exercise = models.ForeignKey(Exercise)
    start = models.FloatField(help_text=_('in km'), default=0)
    length = models.FloatField(help_text=_('in km'), default=0)
    ascent = models.IntegerField(help_text=_('in m'), default=0)
    grade = models.FloatField()
    duration = models.IntegerField()
    speed = models.FloatField()
    est_power = models.FloatField()
    act_power = models.FloatField(default=0)
    power_per_kg = models.FloatField()
    vam = models.IntegerField(default=0)
    category = models.IntegerField()
    avg_hr = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        ''' Calculate extra values before save '''

        self.power_per_kg = self.get_avg_power_kg()
        self.vam = self.get_vam()
        self.category = self.get_category()

        super(Slope, self).save(*args, **kwargs)

    def get_category(self):
        ''' The categories are the same as in the Tour De France or other bike race
        What we do is take the grade of the climb and the distance and multiply them. So, for example, a 2
        kilometer climb at 4% grade = 8000, and 8000 to 16000 is a category 4 climb. 16 to 32 is a category
        3 etc.
        Our categorization is based on the official UCI but with some modification.
        '''
        grade = self.grade * self.length
        if grade < 8000:
            return 5
        elif grade < 16000:
            return 4
        elif grade < 32000:
            return 3
        elif grade < 64000:
            return 2
        elif grade < 128000:
            return 1
        else:
            return 0 # HC ?

    def get_vam(self):
        ''' Return Vertical Ascended Meters / Hour,
        but only if slope category is 3 or lower '''

        ret = 0
        if self.get_category() < 4:
            ret = int(round((float(self.ascent)/self.duration)*3600))
        return ret

    def get_avg_power_kg(self):
        ''' Find weight during exercise and calculate W/kg'''
        userweight = self.exercise.user.get_profile().get_weight(self.exercise.date)
        try:
            if self.act_power:
                return self.act_power/userweight
            return self.est_power / userweight
        except ZeroDivisionError:
            return 0

    def __unicode__(self):
        return u'%s, %s, %s' % (self.exercise, round(self.grade), round(self.length))

    class Meta:
        ordering = ('-exercise__date',)





#class UserProfile(models.Model):
#    user = models.ForeignKey(User, unique=True)
#    height = models.IntegerField(blank=True, help_text=_('in cm'))
#    weight = models.FloatField(blank=True, help_text=_('in kg'))
#    resting_hr = models.IntegerField(blank=True, default=0, help_text=_('beats per minute'))
#    max_hr = models.IntegerField(blank=True, default=0, help_text=_('beats per minute'))
#    motto = models.CharField(max_length=160)
#
#    image = models.ImageField(upload_to='turan', blank=True)
#    cycle = models.CharField(max_length=99, blank=True)
#    cycle_image = models.ImageField(upload_to='turan', blank=True)
#    info = models.TextField(blank=True, help_text=_('textual information'))

#    def __unicode__(self):
#        return unicode(self.user)
#
#    def get_absolute_url(self):
#        return reverse('profile', kwargs={ 'object_id': self.id }) + '/' + slugify(self.user)
#
#    class Meta:
#        verbose_name = _("User Profile")
#        verbose_name_plural = _("User Profiles")
#        ordering = ('user__username',)
#
#
#class UserProfileDetail(models.Model):
#    userprofile = models.ForeignKey(UserProfile)
#    time = models.DateTimeField()
#    weight = models.FloatField(blank=True, null=True, help_text=_('in kg'))
#    resting_hr = models.IntegerField(blank=True,null=True, help_text=_('beats per minute'))
#
#    def save(self, force_insert=False, force_update=False):
#
#        ''' Overriden to update UserProfile with new data '''
#        super(UserProfileDetail, self).save(force_insert, force_update)
#        if self.weight:
#            self.userprofile.weight = int(self.weight)
#        if self.resting_hr:
#            self.userprofile.esting_hr = self.resting_hr
#        self.userprofile.save()

#    def __unicode__(self):
#        return unicode(self.userprofile.user)

#    class Meta:
#        verbose_name = _("User Profile Detail")
#        verbose_name_plural = _("User Profile Details")
#
class Location(models.Model):
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    town = models.CharField(max_length=128, blank=True)
    county = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=128, blank=True)
    country = models.CharField(max_length=128, blank=True)
    url = models.CharField(max_length=128, blank=True, unique=True)

    def __unicode__(self):
        return u'%s (%s, %s) %s' % (self.town, self.lat, self.lon, self.url)

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

def find_nearest_town(lon, lat):
    ''' Iterate saved locations and find nearest town '''

    distance = 99999999
    town = ''

    for loc in Location.objects.all():
        this_distance = proj_distance(lat, lon, loc.lat, loc.lon)
        if this_distance < distance:
            town = loc.town
            distance = this_distance

    return town

# handle notification of new comments
from threadedcomments.models import ThreadedComment
def new_comment(sender, instance, **kwargs):
    if isinstance(instance.content_object, Exercise):
        exercise = instance.content_object
        if notification:
            notification.send([exercise.user], "exercise_comment",
                {"user": instance.user, "exercise": exercise, "comment": instance})
models.signals.post_save.connect(new_comment, sender=ThreadedComment)
