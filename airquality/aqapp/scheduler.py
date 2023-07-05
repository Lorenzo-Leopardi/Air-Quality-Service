import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpResponse
from datetime import datetime
import os
from .models import Measurement
from .models import Sensor


def fetch_data():
    sensor_list = Sensor.objects.all()
    if not sensor_list:
        return
    for sensor in sensor_list:
        r = requests.get(f'http://host.docker.internal:8080/sensors/{sensor.name}/')
        if r.status_code == 200:
            value = r.json()['value']
            is_valid = 0
            if sensor.min_valid <= value <= sensor.max_valid:
                is_valid = 1
            else:
                is_valid = 0

            measurement_obj = Measurement(sensor=sensor,
                                          pollutant=sensor.pollutant,
                                          created=datetime.now(),
                                          value=r.json()['value'],
                                          isValid=is_valid)

            measurement_obj.save()
            return HttpResponse('Yay, it worked')
        return HttpResponse('Could not save data')


def start(interval):
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_data, 'interval', seconds=interval)
    scheduler.start()
