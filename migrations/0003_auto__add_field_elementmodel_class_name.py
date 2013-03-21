# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ElementModel.class_name'
        db.add_column(u'improcflow_elementmodel', 'class_name',
                      self.gf('django.db.models.fields.CharField')(default='element', max_length=120),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ElementModel.class_name'
        db.delete_column(u'improcflow_elementmodel', 'class_name')


    models = {
        u'improcflow.elementmodel': {
            'Meta': {'object_name': 'ElementModel'},
            'class_name': ('django.db.models.fields.CharField', [], {'default': "'element'", 'max_length': '120'}),
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