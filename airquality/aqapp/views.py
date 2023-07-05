import json

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from .models import Measurement
from .models import Pollutant
from .models import Sensor

available_sensors = ['H2S_1', 'H2S_2', 'PM10_1', 'PM10_2']
sensor_not_available = HttpResponseBadRequest('Sensor not available. Available sensors: '+', '.join(available_sensors))


@api_view()
def get_measurements(request, sensor_name):
    sensor_obj = Sensor.objects.get(name=sensor_name)
    if not sensor_obj:
        return HttpResponseBadRequest('This sensor either doesn\'t exist or it can\'t be queried yet.')

    queryset = Measurement.objects.filter(sensor=sensor_obj)
    dictionaries = [obj.as_dict() for obj in queryset]
    return HttpResponse(json.dumps({"data": dictionaries}, indent=4, sort_keys=True, default=str), content_type='application/json')


@csrf_protect
@csrf_exempt
@api_view(['POST'])
@swagger_auto_schema(request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['param1', 'param2'],  # Specify the required parameters here
    properties={
        'sensor_name': openapi.Schema(type=openapi.TYPE_STRING, description='sensor name'),
        'pollutant_name': openapi.Schema(type=openapi.TYPE_STRING, description='pollutant name'),
        'min_valid': openapi.Schema(type=openapi.TYPE_NUMBER, description='minimum valid value for a measurement'),
        'max_valid': openapi.Schema(type=openapi.TYPE_NUMBER, description='maximum valid value for a measurement'),
    }
))
def create_sensor(request):
    if request.method == 'POST':
        post_data = request.POST
        name = post_data.get('sensor_name')
        pollutant = post_data.get('pollutant_name')
        min_valid = float(post_data.get('min_valid'))
        max_valid = float(post_data.get('max_valid'))
    else:
        return HttpResponseBadRequest('Invalid request method.')

    if name not in available_sensors:
        return HttpResponseBadRequest('This sensor name is not available.')

    sensor_obj = Sensor(name=name,
                        pollutant=Pollutant.objects.get(name=pollutant),
                        min_valid=min_valid,
                        max_valid=max_valid)
    sensor_obj.save()

    return HttpResponse(json.dumps({"data": sensor_obj.as_dict()}), content_type='application/json')
