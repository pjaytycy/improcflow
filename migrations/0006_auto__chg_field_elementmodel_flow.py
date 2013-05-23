# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ElementModel.flow'
        db.alter_column(u'improcflow_elementmodel', 'flow_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['improcflow.FlowModel'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ElementModel.flow'
        raise RuntimeError("Cannot reverse this migration. 'ElementModel.flow' and its values cannot be restored.")

    models = {
        u'improcflow.connectionmodel': {
            'Meta': {'object_name': 'ConnectionModel'},
            'dst_connector': ('django.db.models.fields.CharField', [], {'default': "'dst'", 'max_length': '120'}),
            'dst_element': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'connected_as_dst'", 'to': u"orm['improcflow.ElementModel']"}),
            'element': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['improcflow.ElementModel']", 'unique': 'True', 'primary_key': 'True'}),
            'src_connector': ('django.db.models.fields.CharField', [], {'default': "'src'", 'max_length': '120'}),
            'src_element': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'connected_as_src'", 'to': u"orm['improcflow.ElementModel']"})
        },
        u'improcflow.elementmodel': {
            'Meta': {'object_name': 'ElementModel'},
            'class_name': ('django.db.models.fields.CharField', [], {'default': "'element'", 'max_length': '120'}),
            'flow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['improcflow.FlowModel']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'untitled'", 'max_length': '120'})
        },
        u'improcflow.flowmodel': {
            'Meta': {'object_name': 'FlowModel'},
            'element': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['improcflow.ElementModel']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'untitled'", 'max_length': '120'})
        }
    }

    complete_apps = ['improcflow']