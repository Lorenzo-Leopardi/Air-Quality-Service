from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from datetime import datetime
import random

from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.decorators import api_view

from .models import Sensor


def read_sensor(sensor_name):
    today = datetime.now().strftime("%Y%m%d,%H:%M:%S")
    sensor = Sensor.objects.get(name=sensor_name)
    return JsonResponse({"timestamp": today,
                         "value": round(random.uniform(sensor.min_range, sensor.max_range), 1),
                         "pollutant_name": sensor.pollutant})


def config_sensor(request, sensor_name):
    if request.method == 'POST':
        post_data = request.POST
        min_range = float(post_data.get('min_range'))
        max_range = float(post_data.get('max_range'))

        if min_range < 0 or max_range < 0:
            return HttpResponseBadRequest('Invalid parameters. Please provide positive values.')

        Sensor.objects.filter(name=sensor_name).update(min_range=min(min_range, max_range),
                                                       max_range=max(min_range, max_range))
        sensor = Sensor.objects.get(name=sensor_name)
        return JsonResponse({"new_min_range": sensor.min_range,
                             "new_max_range": sensor.max_range})
    else:
        return HttpResponseBadRequest('Invalid request method.')


def H2S_1_read(request):
    return read_sensor("H2S_1")


@csrf_protect
@csrf_exempt
def H2S_1_config(request):
    return config_sensor(request, "H2S_1")


def H2S_2_read(request):
    return read_sensor("H2S_2")


@csrf_protect
@csrf_exempt
def H2S_2_config(request):
    return config_sensor(request, "H2S_2")


def PM10_1_read(request):
    return read_sensor("PM10_1")


@csrf_protect
@csrf_exempt
def PM10_1_config(request):
    return config_sensor(request, "PM10_1")


def PM10_2_read(request):
    return read_sensor("PM10_2")


@csrf_protect
@csrf_exempt
def PM10_2_config(request):
    return config_sensor(request, "PM10_2")
