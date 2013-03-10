# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ElementModel'
        db.create_table(u'improcflow_elementmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='untitled', max_length=120)),
            ('flow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['improcflow.FlowModel'])),
        ))
        db.send_create_signal(u'improcflow', ['ElementModel'])


    def backwards(self, orm):
        # Deleting model 'ElementModel'
        db.delete_table(u'improcflow_elementmodel')


    models = {
        u'improcflow.elementmodel': {
            'Meta': {'object_name': 'ElementModel'},
            'flow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['improcflow.FlowModel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'untitled'", 'max_length': '120'})
        },
        u'improcflow.flowmodel': {
            'Meta': {'object_name': 'FlowModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'untitled'", 'max_length': '120'})
        }
    }

    complete_apps = ['improcflow']