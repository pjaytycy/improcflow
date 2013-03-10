# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FlowModel'
        db.create_table(u'improcflow_flowmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='untitled', max_length=120)),
        ))
        db.send_create_signal(u'improcflow', ['FlowModel'])


    def backwards(self, orm):
        # Deleting model 'FlowModel'
        db.delete_table(u'improcflow_flowmodel')


    models = {
        u'improcflow.flowmodel': {
            'Meta': {'object_name': 'FlowModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'untitled'", 'max_length': '120'})
        }
    }

    complete_apps = ['improcflow']