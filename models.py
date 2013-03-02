import numpy

DEBUG = False

from django.db import models

def combine_title(part1, part2):
  if part1 is None:
    return None
  if part2 is None:
    return None
  return str(part1) + "." + str(part2)


class Connector(object):
  def __init__(self, title = None):
    self.value = None
    self.valid = False
    self.title = title
    
  def set_value(self, value):
    self.value = value
    self.valid = True
  
  def is_ready(self):
    return self.valid

    
class Element(object):
  def __init__(self, title = None):
    self.title = title
    self.input_connectors = []
    self.output_connectors = []
    
  def add_input_connector(self, title = None):
    input_connector = Connector(title = combine_title(self.title, title))
    self.input_connectors.append(input_connector)
    return input_connector
  
  def add_output_connector(self, title = None):
    output_connector = Connector(title = combine_title(self.title, title))
    self.output_connectors.append(output_connector)
    return output_connector
  
  def replace_input_connector(self, old_input_connector, new_input_connector):
    self.input_connectors.remove(old_input_connector)
    self.input_connectors.append(new_input_connector)
    return new_input_connector
  
  def replace_output_connector(self, old_output_connector, new_output_connector):
    self.output_connectors.remove(old_output_connector)
    self.output_connectors.append(new_output_connector)
    return new_output_connector
    
  def run(self):
    if DEBUG:
      print "%s %s run" % (self.__class__.__name__, self.title)
  
  def is_ready(self):
    for input_connector in self.input_connectors:
      if not(input_connector.is_ready()):
        return False
    return True
    
  
class Connection(Element):
  def __init__(self, title = None):
    super(Connection, self).__init__(title = title)
    self.src = self.add_input_connector()
    self.dst = self.add_output_connector()
  
  def set_src_dst(self, src, dst):
    self.src = self.replace_input_connector(self.src, src)
    self.dst = self.replace_output_connector(self.dst, dst)
        
  def run(self):
    super(Connection, self).run()
    if DEBUG:
      print "  Connection %s from %s to %s" % (self.title, self.src.title, self.dst.title)
    self.dst.set_value(self.src.value)

    
class InputImage(Element):
  def __init__(self, title = None):
    super(InputImage, self).__init__(title = title)
    self.image = self.add_input_connector(title = "image")

  def set_value(self, src):
    self.image.set_value(src)
    
    
class OpenCVMean(Element):
  def __init__(self, title = None):
    super(OpenCVMean, self).__init__(title = title)
    self.src = self.add_input_connector(title = "src")
    self.mean = self.add_output_connector(title = "mean")
    
  def run(self):
    super(OpenCVMean, self).run()
    self.mean.set_value(numpy.average(self.src.value))
    
  
class OutputNumber(Element):
  def __init__(self, title = None):
    super(OutputNumber, self).__init__(title = title)
    self.number = self.add_input_connector(title = "number")
      
  def result(self):
    return self.number.value
    
  
class Flow(object):
  def __init__(self):
    self.elements = []
  
  def addElement(self, element):
    self.elements.append(element)
  
  def connect(self, src, dst, title = None):
    connection = Connection(title = title)
    connection.set_src_dst(src, dst)
    self.elements.append(connection)
  
  def run(self, elements_to_do = None):
    if elements_to_do is None:
      elements_to_do = self.elements[:]
    
    elements_left = []
    elements_done = 0
    for element in elements_to_do:
      if element.is_ready():
        element.run()
        elements_done += 1
      else:
        elements_left.append(element)
    
    if elements_done == 0:
      return True
    
    return self.run(elements_left)
  
  
############
## import datetime
## 
## from django.db import models
## from django.utils import timezone
## 
## class Poll(models.Model):
##   question = models.CharField(max_length = 200)
##   pub_date = models.DateTimeField('date published')
##   
##   def was_published_recently(self):
##     now = timezone.now()
##     delta = datetime.timedelta(days = 1)
##     return now - delta <= self.pub_date < now
##   
##   was_published_recently.admin_order_field = "pub_date"
##   was_published_recently.boolean = True
##   was_published_recently.short_description = "Published recently?"
##   
##   def __unicode__(self):
##     return self.question
## 
## class Choice(models.Model):
##   poll = models.ForeignKey(Poll)
##   choice_text = models.CharField(max_length = 200)
##   votes = models.IntegerField(default = 0)
##   
##   def __unicode__(self):
##     return self.choice_text
