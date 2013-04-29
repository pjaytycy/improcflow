from django.db import models

class FlowModel(models.Model):
  title = models.CharField(max_length = 120, default = "untitled")
  
  def __unicode__(self):
    return self.title
    

class ElementModel(models.Model):
  title = models.CharField(max_length = 120, default = "untitled")
  flow = models.ForeignKey(FlowModel)
  class_name = models.CharField(max_length = 120, default = "element")
  
  def __unicode__(self):
    return "%s::%s" % (self.class_name, self.title)
    

class ConnectionModel(models.Model):
  element = models.OneToOneField(ElementModel, primary_key = True)
  src_element = models.ForeignKey(ElementModel, related_name = "connected_as_src")
  src_connector = models.CharField(max_length = 120, default = "src")
  dst_element = models.ForeignKey(ElementModel, related_name = "connected_as_dst")
  dst_connector = models.CharField(max_length = 120, default = "dst")
  
  def __unicode__(self):
    return "%s from %s::%s to %s::%s" % (self.element, 
             self.src_element, self.src_connector, 
             self.dst_element, self.dst_connector)
