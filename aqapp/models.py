from django.db import models


# Create your models here.
class Sensor(models.Model):
    name = models.CharField(max_length=25, unique=True, null=True)
    pollutant = models.CharField(max_length=10, null=True)
    min_range = models.FloatField(default=0)
    max_range = models.FloatField(default=100)
