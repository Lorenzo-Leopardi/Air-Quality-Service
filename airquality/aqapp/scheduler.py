import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpResponse
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from .serializers import MeasurementSerializer
from .models import Sensor


def fetch_data():
    sensor_list = Sensor.objects.all()
    if not sensor_list:
        return

    serializer_list =[]
    for sensor in sensor_list:
        url = f'http://host.docker.internal:8080/sensors/{sensor.name}/'
        response = requests.get(url)

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            value = data['value']
            is_valid = 0 if not (sensor.min_valid <= value <= sensor.max_valid) else 1

            measurement_data = {
                'sensor': sensor.pk,
                'pollutant': sensor.pollutant.pk,
                'created': datetime.now(),
                'value': value,
                'isValid': is_valid
            }

            serializer = MeasurementSerializer(data=measurement_data)
            if serializer.is_valid():
                serializer.save()

        else:
            return Response('Could not save Measurement', status=status.HTTP_400_BAD_REQUEST)

    return Response('Measurement(s) saved', status=status.HTTP_200_OK)


def start(interval):
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_data, 'interval', seconds=interval)
    scheduler.start()
