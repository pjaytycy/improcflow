from django.db import models

class FlowModel(models.Model):
  element = models.OneToOneField('ElementModel', primary_key = True)
  title = models.CharField(max_length = 120, default = "untitled")
  
  def __unicode__(self):
    return self.title
    

class ElementGroupModel(models.Model):
  title = models.CharField(max_length = 120, default = "untitled")
  
  def __unicode__(self):
    return "ElementGroup::%s" % self.title
    
  
class ElementModel(models.Model):
  title = models.CharField(max_length = 120, default = "untitled")
  flow = models.ForeignKey(FlowModel, null = True)
  class_name = models.CharField(max_length = 120, default = "element")
  group = models.ForeignKey(ElementGroupModel, null = True)
  
  def __unicode__(self):
    return "%s::%s::%s" % (self.group, self.class_name, self.title)
    
    
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
