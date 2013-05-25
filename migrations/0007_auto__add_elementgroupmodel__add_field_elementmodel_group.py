# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ElementGroupModel'
        db.create_table(u'improcflow_elementgroupmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='untitled', max_length=120)),
        ))
        db.send_create_signal(u'improcflow', ['ElementGroupModel'])

        # Adding field 'ElementModel.group'
        db.add_column(u'improcflow_elementmodel', 'group',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['improcflow.ElementGroupModel'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'ElementGroupModel'
        db.delete_table(u'improcflow_elementgroupmodel')

        # Deleting field 'ElementModel.group'
        db.delete_column(u'improcflow_elementmodel', 'group_id')


    models = {
        u'improcflow.connectionmodel': {
            'Meta': {'object_name': 'ConnectionModel'},
            'dst_connector': ('django.db.models.fields.CharField', [], {'default': "'dst'", 'max_length': '120'}),
            'dst_element': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'connected_as_dst'", 'to': u"orm['improcflow.ElementModel']"}),
            'element': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['improcflow.ElementModel']", 'unique': 'True', 'primary_key': 'True'}),
            'src_connector': ('django.db.models.fields.CharField', [], {'default': "'src'", 'max_length': '120'}),
            'src_element': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'connected_as_src'", 'to': u"orm['improcflow.ElementModel']"})
        },
        u'improcflow.elementgroupmodel': {
            'Meta': {'object_name': 'ElementGroupModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'untitled'", 'max_length': '120'})
        },
        u'improcflow.elementmodel': {
            'Meta': {'object_name': 'ElementModel'},
            'class_name': ('django.db.models.fields.CharField', [], {'default': "'element'", 'max_length': '120'}),
            'flow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['improcflow.FlowModel']", 'null': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['improcflow.ElementGroupModel']", 'null': 'True'}),
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