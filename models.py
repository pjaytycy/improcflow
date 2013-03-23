from django.db import models

class FlowModel(models.Model):
  title = models.CharField(max_length = 120, default = "untitled")

class ElementModel(models.Model):
  title = models.CharField(max_length = 120, default = "untitled")
  flow = models.ForeignKey(FlowModel)
  class_name = models.CharField(max_length = 120, default = "element")

class ConnectionModel(models.Model):
  element = models.OneToOneField(ElementModel, primary_key = True)
  src_element = models.ForeignKey(ElementModel, related_name = "connected_as_src")
  src_connector = models.CharField(max_length = 120, default = "src")
  dst_element = models.ForeignKey(ElementModel, related_name = "connected_as_dst")
  dst_connector = models.CharField(max_length = 120, default = "dst")
