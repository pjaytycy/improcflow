# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ConnectionModel'
        db.create_table(u'improcflow_connectionmodel', (
            ('element', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['improcflow.ElementModel'], unique=True, primary_key=True)),
            ('src_element', self.gf('django.db.models.fields.related.ForeignKey')(related_name='connected_as_src', to=orm['improcflow.ElementModel'])),
            ('src_connector', self.gf('django.db.models.fields.CharField')(default='unknown', max_length=120)),
            ('dst_element', self.gf('django.db.models.fields.related.ForeignKey')(related_name='connected_as_dst', to=orm['improcflow.ElementModel'])),
            ('dst_connector', self.gf('django.db.models.fields.CharField')(default='unknown', max_length=120)),
        ))
        db.send_create_signal(u'improcflow', ['ConnectionModel'])


    def backwards(self, orm):
        # Deleting model 'ConnectionModel'
        db.delete_table(u'improcflow_connectionmodel')


    models = {
        u'improcflow.connectionmodel': {
            'Meta': {'object_name': 'ConnectionModel'},
            'dst_connector': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '120'}),
            'dst_element': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'connected_as_dst'", 'to': u"orm['improcflow.ElementModel']"}),
            'element': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['improcflow.ElementModel']", 'unique': 'True', 'primary_key': 'True'}),
            'src_connector': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '120'}),
            'src_element': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'connected_as_src'", 'to': u"orm['improcflow.ElementModel']"})
        },
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