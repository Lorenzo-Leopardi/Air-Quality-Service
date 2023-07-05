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

    def as_dict(self):
        return {"name": self.name,
                "pollutant": self.pollutant.name,
                "min_valid": self.min_valid,
                "max_valid": self.max_valid}


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    pollutant = models.ForeignKey(Pollutant, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    value = models.FloatField(null=True)
    isValid = models.IntegerField(default=0)

    def as_dict(self):
        return {"created": self.created,
                "pollutant": self.pollutant.name,
                "sensor": self.sensor.name,
                "value": self.value,
                "isValid": self.isValid}