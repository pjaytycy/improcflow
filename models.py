from django.db import models

class FlowModel(models.Model):
  title = models.CharField(max_length = 120, default = "untitled")
