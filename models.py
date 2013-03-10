from django.db import models

class FlowModel(models.Model):
  title = models.CharField(max_length = 120, default = "untitled")

class ElementModel(models.Model):
  title = models.CharField(max_length = 120, default = "untitled")
  flow = models.ForeignKey(FlowModel)
  