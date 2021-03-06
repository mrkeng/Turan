# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Route'
        db.create_table('turan_route', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=160, blank=True)),
            ('distance', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('route_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('gpx_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('ascent', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('descent', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('start_lat', self.gf('django.db.models.fields.FloatField')(default=0.0, blank=True)),
            ('start_lon', self.gf('django.db.models.fields.FloatField')(default=0.0, blank=True)),
            ('end_lat', self.gf('django.db.models.fields.FloatField')(default=0.0, blank=True)),
            ('end_lon', self.gf('django.db.models.fields.FloatField')(default=0.0, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('single_serving', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tags', self.gf('tagging.fields.TagField')()),
        ))
        db.send_create_signal('turan', ['Route'])

        # Adding model 'ExerciseType'
        db.create_table('turan_exercisetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('altitude', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slopes', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('turan', ['ExerciseType'])

        # Adding model 'Exercise'
        db.create_table('turan_exercise', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('exercise_type', self.gf('django.db.models.fields.related.ForeignKey')(default=13, to=orm['turan.ExerciseType'])),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['turan.Route'], null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.DecimalField')(default=0, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('avg_speed', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('avg_cadence', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('avg_pedaling_cad', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('avg_power', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('avg_pedaling_power', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_speed', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('max_cadence', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_power', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('avg_hr', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_hr', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('kcal', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('temperature', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('sensor_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('exercise_permission', self.gf('django.db.models.fields.CharField')(default='A', max_length=1)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
        ))
        db.send_create_signal('turan', ['Exercise'])

        # Adding model 'ExercisePermission'
        db.create_table('turan_exercisepermission', (
            ('exercise', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['turan.Exercise'], unique=True, primary_key=True)),
            ('speed', self.gf('django.db.models.fields.CharField')(default='A', max_length=1)),
            ('power', self.gf('django.db.models.fields.CharField')(default='A', max_length=1)),
            ('cadence', self.gf('django.db.models.fields.CharField')(default='A', max_length=1)),
            ('hr', self.gf('django.db.models.fields.CharField')(default='A', max_length=1)),
        ))
        db.send_create_signal('turan', ['ExercisePermission'])

        # Adding model 'ExerciseDetail'
        db.create_table('turan_exercisedetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exercise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['turan.Exercise'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('speed', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('hr', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('altitude', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lon', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('cadence', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('power', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('turan', ['ExerciseDetail'])

        # Adding model 'BestPowerEffort'
        db.create_table('turan_bestpowereffort', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exercise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['turan.Exercise'])),
            ('pos', self.gf('django.db.models.fields.FloatField')()),
            ('length', self.gf('django.db.models.fields.FloatField')()),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
            ('power', self.gf('django.db.models.fields.IntegerField')()),
            ('ascent', self.gf('django.db.models.fields.IntegerField')()),
            ('descent', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('turan', ['BestPowerEffort'])

        # Adding model 'BestSpeedEffort'
        db.create_table('turan_bestspeedeffort', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exercise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['turan.Exercise'])),
            ('pos', self.gf('django.db.models.fields.FloatField')()),
            ('length', self.gf('django.db.models.fields.FloatField')()),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
            ('speed', self.gf('django.db.models.fields.FloatField')()),
            ('ascent', self.gf('django.db.models.fields.IntegerField')()),
            ('descent', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('turan', ['BestSpeedEffort'])

        # Adding model 'MergeSensorFile'
        db.create_table('turan_mergesensorfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exercise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['turan.Exercise'])),
            ('merge_strategy', self.gf('django.db.models.fields.CharField')(default='M', max_length=1)),
            ('sensor_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('hr', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('power', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cadence', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('altitude', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('position', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('speed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('turan', ['MergeSensorFile'])

        # Adding model 'Slope'
        db.create_table('turan_slope', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exercise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['turan.Exercise'])),
            ('start', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('length', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('ascent', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('grade', self.gf('django.db.models.fields.FloatField')()),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
            ('speed', self.gf('django.db.models.fields.FloatField')()),
            ('est_power', self.gf('django.db.models.fields.FloatField')()),
            ('act_power', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('power_per_kg', self.gf('django.db.models.fields.FloatField')()),
            ('vam', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('category', self.gf('django.db.models.fields.IntegerField')()),
            ('avg_hr', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('turan', ['Slope'])

        # Adding model 'Location'
        db.create_table('turan_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lon', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('town', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128, blank=True)),
        ))
        db.send_create_signal('turan', ['Location'])


    def backwards(self, orm):
        
        # Deleting model 'Route'
        db.delete_table('turan_route')

        # Deleting model 'ExerciseType'
        db.delete_table('turan_exercisetype')

        # Deleting model 'Exercise'
        db.delete_table('turan_exercise')

        # Deleting model 'ExercisePermission'
        db.delete_table('turan_exercisepermission')

        # Deleting model 'ExerciseDetail'
        db.delete_table('turan_exercisedetail')

        # Deleting model 'BestPowerEffort'
        db.delete_table('turan_bestpowereffort')

        # Deleting model 'BestSpeedEffort'
        db.delete_table('turan_bestspeedeffort')

        # Deleting model 'MergeSensorFile'
        db.delete_table('turan_mergesensorfile')

        # Deleting model 'Slope'
        db.delete_table('turan_slope')

        # Deleting model 'Location'
        db.delete_table('turan_location')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'turan.bestpowereffort': {
            'Meta': {'ordering': "('duration',)", 'object_name': 'BestPowerEffort'},
            'ascent': ('django.db.models.fields.IntegerField', [], {}),
            'descent': ('django.db.models.fields.IntegerField', [], {}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['turan.Exercise']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {}),
            'pos': ('django.db.models.fields.FloatField', [], {}),
            'power': ('django.db.models.fields.IntegerField', [], {})
        },
        'turan.bestspeedeffort': {
            'Meta': {'ordering': "('duration',)", 'object_name': 'BestSpeedEffort'},
            'ascent': ('django.db.models.fields.IntegerField', [], {}),
            'descent': ('django.db.models.fields.IntegerField', [], {}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['turan.Exercise']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {}),
            'pos': ('django.db.models.fields.FloatField', [], {}),
            'speed': ('django.db.models.fields.FloatField', [], {})
        },
        'turan.exercise': {
            'Meta': {'ordering': "('-date', '-time')", 'object_name': 'Exercise'},
            'avg_cadence': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avg_hr': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avg_pedaling_cad': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avg_pedaling_power': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avg_power': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avg_speed': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.DecimalField', [], {'default': '0', 'blank': 'True'}),
            'exercise_permission': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'exercise_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '13', 'to': "orm['turan.ExerciseType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kcal': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'max_cadence': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_hr': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_power': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_speed': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['turan.Route']", 'null': 'True', 'blank': 'True'}),
            'sensor_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'turan.exercisedetail': {
            'Meta': {'ordering': "('time',)", 'object_name': 'ExerciseDetail'},
            'altitude': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cadence': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['turan.Exercise']"}),
            'hr': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'power': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'speed': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'turan.exercisepermission': {
            'Meta': {'object_name': 'ExercisePermission'},
            'cadence': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'exercise': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['turan.Exercise']", 'unique': 'True', 'primary_key': 'True'}),
            'hr': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'power': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'speed': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'})
        },
        'turan.exercisetype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ExerciseType'},
            'altitude': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'slopes': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'turan.location': {
            'Meta': {'object_name': 'Location'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'blank': 'True'})
        },
        'turan.mergesensorfile': {
            'Meta': {'object_name': 'MergeSensorFile'},
            'altitude': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cadence': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['turan.Exercise']"}),
            'hr': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merge_strategy': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '1'}),
            'position': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'power': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sensor_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'speed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'turan.route': {
            'Meta': {'ordering': "('-created', 'name')", 'object_name': 'Route'},
            'ascent': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'descent': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'distance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'end_lat': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'end_lon': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'gpx_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'route_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'single_serving': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start_lat': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'start_lon': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {})
        },
        'turan.slope': {
            'Meta': {'ordering': "('-exercise__date',)", 'object_name': 'Slope'},
            'act_power': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'ascent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'avg_hr': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.IntegerField', [], {}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'est_power': ('django.db.models.fields.FloatField', [], {}),
            'exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['turan.Exercise']"}),
            'grade': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'power_per_kg': ('django.db.models.fields.FloatField', [], {}),
            'speed': ('django.db.models.fields.FloatField', [], {}),
            'start': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'vam': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['turan']
