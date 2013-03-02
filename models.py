import numpy

from django.db import models

class InputImage(models.Model):
  image = None
  
  def __init__(self, src):
    self.image = src

class OpenCVMean(models.Model):
  src = None
  mean = None
  
class OutputNumber(models.Model):
  number = 3.5
  
class Flow(models.Model):
  def addElement(self, element):
    if type(element) == InputImage:
      self.src = element.image
    if type(element) == OutputNumber:
      self.dst = element
  
  def connect(self, src, dst):
    pass
  
  def run(self):
    result = numpy.average(self.src)
    self.dst.number = result
  
  
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
