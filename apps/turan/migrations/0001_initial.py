
from south.db import db
from django.db import models
from turan.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'CycleTripDetail'
        db.create_table('turan_cycletripdetail', (
            ('id', orm['turan.CycleTripDetail:id']),
            ('time', orm['turan.CycleTripDetail:time']),
            ('speed', orm['turan.CycleTripDetail:speed']),
            ('hr', orm['turan.CycleTripDetail:hr']),
            ('altitude', orm['turan.CycleTripDetail:altitude']),
            ('lat', orm['turan.CycleTripDetail:lat']),
            ('lon', orm['turan.CycleTripDetail:lon']),
            ('trip', orm['turan.CycleTripDetail:trip']),
            ('cadence', orm['turan.CycleTripDetail:cadence']),
        ))
        db.send_create_signal('turan', ['CycleTripDetail'])
        
        # Adding model 'ExerciseType'
        db.create_table('turan_exercisetype', (
            ('id', orm['turan.ExerciseType:id']),
            ('name', orm['turan.ExerciseType:name']),
        ))
        db.send_create_signal('turan', ['ExerciseType'])
        
        # Adding model 'HikeDetail'
        db.create_table('turan_hikedetail', (
            ('id', orm['turan.HikeDetail:id']),
            ('time', orm['turan.HikeDetail:time']),
            ('speed', orm['turan.HikeDetail:speed']),
            ('hr', orm['turan.HikeDetail:hr']),
            ('altitude', orm['turan.HikeDetail:altitude']),
            ('lat', orm['turan.HikeDetail:lat']),
            ('lon', orm['turan.HikeDetail:lon']),
            ('trip', orm['turan.HikeDetail:trip']),
        ))
        db.send_create_signal('turan', ['HikeDetail'])
        
        # Adding model 'CycleTrip'
        db.create_table('turan_cycletrip', (
            ('id', orm['turan.CycleTrip:id']),
            ('user', orm['turan.CycleTrip:user']),
            ('route', orm['turan.CycleTrip:route']),
            ('duration', orm['turan.CycleTrip:duration']),
            ('date', orm['turan.CycleTrip:date']),
            ('time', orm['turan.CycleTrip:time']),
            ('comment', orm['turan.CycleTrip:comment']),
            ('url', orm['turan.CycleTrip:url']),
            ('avg_hr', orm['turan.CycleTrip:avg_hr']),
            ('max_hr', orm['turan.CycleTrip:max_hr']),
            ('kcal', orm['turan.CycleTrip:kcal']),
            ('sensor_file', orm['turan.CycleTrip:sensor_file']),
            ('object_id', orm['turan.CycleTrip:object_id']),
            ('content_type', orm['turan.CycleTrip:content_type']),
            ('avg_speed', orm['turan.CycleTrip:avg_speed']),
            ('avg_cadence', orm['turan.CycleTrip:avg_cadence']),
            ('max_speed', orm['turan.CycleTrip:max_speed']),
            ('max_cadence', orm['turan.CycleTrip:max_cadence']),
        ))
        db.send_create_signal('turan', ['CycleTrip'])
        
        # Adding model 'OtherExercise'
        db.create_table('turan_otherexercise', (
            ('id', orm['turan.OtherExercise:id']),
            ('user', orm['turan.OtherExercise:user']),
            ('route', orm['turan.OtherExercise:route']),
            ('duration', orm['turan.OtherExercise:duration']),
            ('date', orm['turan.OtherExercise:date']),
            ('time', orm['turan.OtherExercise:time']),
            ('comment', orm['turan.OtherExercise:comment']),
            ('url', orm['turan.OtherExercise:url']),
            ('avg_hr', orm['turan.OtherExercise:avg_hr']),
            ('max_hr', orm['turan.OtherExercise:max_hr']),
            ('kcal', orm['turan.OtherExercise:kcal']),
            ('sensor_file', orm['turan.OtherExercise:sensor_file']),
            ('object_id', orm['turan.OtherExercise:object_id']),
            ('content_type', orm['turan.OtherExercise:content_type']),
            ('exercise_type', orm['turan.OtherExercise:exercise_type']),
        ))
        db.send_create_signal('turan', ['OtherExercise'])
        
        # Adding model 'OtherExerciseDetail'
        db.create_table('turan_otherexercisedetail', (
            ('id', orm['turan.OtherExerciseDetail:id']),
            ('time', orm['turan.OtherExerciseDetail:time']),
            ('speed', orm['turan.OtherExerciseDetail:speed']),
            ('hr', orm['turan.OtherExerciseDetail:hr']),
            ('altitude', orm['turan.OtherExerciseDetail:altitude']),
            ('lat', orm['turan.OtherExerciseDetail:lat']),
            ('lon', orm['turan.OtherExerciseDetail:lon']),
            ('trip', orm['turan.OtherExerciseDetail:trip']),
        ))
        db.send_create_signal('turan', ['OtherExerciseDetail'])
        
        # Adding model 'Route'
        db.create_table('turan_route', (
            ('id', orm['turan.Route:id']),
            ('name', orm['turan.Route:name']),
            ('distance', orm['turan.Route:distance']),
            ('description', orm['turan.Route:description']),
            ('route_url', orm['turan.Route:route_url']),
            ('gpx_file', orm['turan.Route:gpx_file']),
            ('ascent', orm['turan.Route:ascent']),
            ('descent', orm['turan.Route:descent']),
            ('start_lat', orm['turan.Route:start_lat']),
            ('start_lon', orm['turan.Route:start_lon']),
            ('end_lat', orm['turan.Route:end_lat']),
            ('end_lon', orm['turan.Route:end_lon']),
            ('created', orm['turan.Route:created']),
            ('single_serving', orm['turan.Route:single_serving']),
            ('tags', orm['turan.Route:tags']),
        ))
        db.send_create_signal('turan', ['Route'])
        
        # Adding model 'Location'
        db.create_table('turan_location', (
            ('id', orm['turan.Location:id']),
            ('lat', orm['turan.Location:lat']),
            ('lon', orm['turan.Location:lon']),
            ('town', orm['turan.Location:town']),
            ('county', orm['turan.Location:county']),
            ('state', orm['turan.Location:state']),
            ('country', orm['turan.Location:country']),
            ('url', orm['turan.Location:url']),
        ))
        db.send_create_signal('turan', ['Location'])
        
        # Adding model 'Hike'
        db.create_table('turan_hike', (
            ('id', orm['turan.Hike:id']),
            ('user', orm['turan.Hike:user']),
            ('route', orm['turan.Hike:route']),
            ('duration', orm['turan.Hike:duration']),
            ('date', orm['turan.Hike:date']),
            ('time', orm['turan.Hike:time']),
            ('comment', orm['turan.Hike:comment']),
            ('url', orm['turan.Hike:url']),
            ('avg_hr', orm['turan.Hike:avg_hr']),
            ('max_hr', orm['turan.Hike:max_hr']),
            ('kcal', orm['turan.Hike:kcal']),
            ('sensor_file', orm['turan.Hike:sensor_file']),
            ('object_id', orm['turan.Hike:object_id']),
            ('content_type', orm['turan.Hike:content_type']),
            ('avg_speed', orm['turan.Hike:avg_speed']),
            ('max_speed', orm['turan.Hike:max_speed']),
        ))
        db.send_create_signal('turan', ['Hike'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'CycleTripDetail'
        db.delete_table('turan_cycletripdetail')
        
        # Deleting model 'ExerciseType'
        db.delete_table('turan_exercisetype')
        
        # Deleting model 'HikeDetail'
        db.delete_table('turan_hikedetail')
        
        # Deleting model 'CycleTrip'
        db.delete_table('turan_cycletrip')
        
        # Deleting model 'OtherExercise'
        db.delete_table('turan_otherexercise')
        
        # Deleting model 'OtherExerciseDetail'
        db.delete_table('turan_otherexercisedetail')
        
        # Deleting model 'Route'
        db.delete_table('turan_route')
        
        # Deleting model 'Location'
        db.delete_table('turan_location')
        
        # Deleting model 'Hike'
        db.delete_table('turan_hike')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'turan.cycletrip': {
            'avg_cadence': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avg_hr': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avg_speed': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'duration': ('DurationField', [], {'default': '0', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kcal': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'max_cadence': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_hr': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_speed': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['turan.Route']"}),
            'sensor_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'turan.cycletripdetail': {
            'altitude': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cadence': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hr': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'speed': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['turan.CycleTrip']"})
        },
        'turan.exercisetype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'turan.hike': {
            'avg_hr': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avg_speed': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'duration': ('DurationField', [], {'default': '0', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kcal': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'max_hr': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_speed': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['turan.Route']"}),
            'sensor_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'turan.hikedetail': {
            'altitude': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hr': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'speed': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['turan.Hike']"})
        },
        'turan.location': {
            'country': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'blank': 'True'})
        },
        'turan.otherexercise': {
            'avg_hr': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'duration': ('DurationField', [], {'default': '0', 'blank': 'True'}),
            'exercise_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['turan.ExerciseType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kcal': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'max_hr': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['turan.Route']"}),
            'sensor_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'turan.otherexercisedetail': {
            'altitude': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hr': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'speed': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['turan.OtherExercise']"})
        },
        'turan.route': {
            'ascent': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'descent': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'distance': ('django.db.models.fields.FloatField', [], {}),
            'end_lat': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'end_lon': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'gpx_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'route_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'single_serving': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'start_lat': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'start_lon': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'tags': ('TagField', [], {})
        }
    }
    
    complete_apps = ['turan']
