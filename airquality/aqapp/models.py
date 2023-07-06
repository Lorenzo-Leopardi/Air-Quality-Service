from datetime import datetime
from django.db import models


class Pollutant(models.Model):
    name = models.CharField(max_length=25, unique=True, null=True)

    def as_dict(self):
        return {"name": self.name}


class Sensor(models.Model):
    name = models.CharField(max_length=25, unique=True, null=True)
    pollutant = models.ForeignKey(Pollutant, on_delete=models.CASCADE, null=True)
    min_valid = models.FloatField(default=0)
    max_valid = models.FloatField(default=100)



class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    pollutant = models.ForeignKey(Pollutant, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    value = models.FloatField(null=True)
    isValid = models.IntegerField(choices=[(0, '0'), (1, '1')], default=0)
