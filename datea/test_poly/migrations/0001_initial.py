# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Meal'
        db.create_table('test_poly_meal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
        ))
        db.send_create_signal('test_poly', ['Meal'])

        # Adding model 'Salad'
        db.create_table('test_poly_salad', (
            ('meal_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['test_poly.Meal'], unique=True, primary_key=True)),
            ('too_leafy', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('test_poly', ['Salad'])


    def backwards(self, orm):
        # Deleting model 'Meal'
        db.delete_table('test_poly_meal')

        # Deleting model 'Salad'
        db.delete_table('test_poly_salad')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'test_poly.meal': {
            'Meta': {'object_name': 'Meal'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        },
        'test_poly.salad': {
            'Meta': {'object_name': 'Salad', '_ormbases': ['test_poly.Meal']},
            'meal_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['test_poly.Meal']", 'unique': 'True', 'primary_key': 'True'}),
            'too_leafy': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['test_poly']