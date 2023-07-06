from datetime import datetime, timedelta

from django.db.models import Avg
from django.http import HttpResponseBadRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter, inline_serializer
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Pollutant, Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer

available_sensors = ['H2S_1', 'H2S_2', 'PM10_1', 'PM10_2']
sensor_not_available = HttpResponseBadRequest(
    'Sensor not available. Available sensors: ' + ', '.join(available_sensors))


class PollutantAverageView(APIView):
    @extend_schema(
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='Average',
                fields={
                    "pollutant": serializers.CharField(),
                    "average": serializers.FloatField()
                }
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='This sensor either doesn\'t exist or it can\'t be queried yet.'),
        },
        parameters=[
            OpenApiParameter(
                name='time_range',
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Number of hours to compute the average over',
                examples=[
                    OpenApiExample(
                        name='Example value',
                        value='8'
                    ),
                ],
            ),
            OpenApiParameter(
                name='start_time',
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                description='Date and time to start the average calculation',
                examples=[
                    OpenApiExample(
                        name='Example value',
                        value='2023-07-21T23:45:59'
                    ),
                ],
            ),
        ],
    )
    def get(self, request, pollutant_name):
        """
        Returns the average of measurements for a pollutant.
        If only the time_range parameter is provided, the average is computed by sliding.
        If the start_time parameter is provided too, the average is computed by tumbling (back in time).
        """
        try:
            pollutant_obj = Pollutant.objects.get(name=pollutant_name)
        except Pollutant.DoesNotExist:
            return Response('This pollutant doesn\'t exist.', status=status.HTTP_400_BAD_REQUEST)

        time_range = int(request.GET.get('time_range'))
        if 'start_time' in request.GET:
            start_time = datetime.strptime(request.GET.get('start_time'), "%Y-%m-%dT%H:%M:%S")
            # Tumbling
            queryset = Measurement.objects.filter(pollutant=pollutant_obj,
                                                  created__range=[start_time - timedelta(hours=time_range), start_time])
        else:
            # Sliding
            queryset = Measurement.objects.filter(pollutant=pollutant_obj,
                                                  created__range=[datetime.now() - timedelta(hours=time_range),
                                                                  datetime.now()])

        average = queryset.aggregate(Avg("value"))['value__avg']
        return Response({"pollutant": pollutant_name, "average": average})


class MeasurementsView(APIView):
    @extend_schema(
        responses={
            status.HTTP_200_OK: MeasurementSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='This sensor either doesn\'t exist or it can\'t be queried yet.'),
        },
        parameters=[
            OpenApiParameter(
                name='start_time',
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                description='Return measurements from this time onwards',
                examples=[
                    OpenApiExample(
                        name='Example value',
                        value='2023-07-05T17:32:28'
                    ),
                ],
            ),
            OpenApiParameter(
                name='end_time',
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                description='Return measurements up until this time',
                examples=[
                    OpenApiExample(
                        name='Example value',
                        value='2023-07-21T23:45:59'
                    ),
                ],
            ),
        ],
    )
    def get(self, request, sensor_name):
        """
        Returns a list of measurements for this sensor.
        If both time range parameters are provided, measurements can be filtered by time
        """
        try:
            sensor_obj = Sensor.objects.get(name=sensor_name)
        except Sensor.DoesNotExist:
            return Response('This sensor either doesn\'t exist or it can\'t be queried yet.',
                            status=status.HTTP_400_BAD_REQUEST)

        if 'start_time' in request.GET and 'end_time' in request.GET:
            start_time = datetime.strptime(request.GET.get('start_time'), "%Y-%m-%dT%H:%M:%S")
            end_time = datetime.strptime(request.GET.get('end_time'), "%Y-%m-%dT%H:%M:%S")
            queryset = Measurement.objects.filter(sensor=sensor_obj, created__range=[start_time, end_time])
        else:
            queryset = Measurement.objects.filter(sensor=sensor_obj)

        serializer = MeasurementSerializer(queryset, many=True)
        return Response({"data": serializer.data})


class SensorCreateView(APIView):
    @extend_schema(
        request=SensorSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(response=SensorSerializer),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description='Bad request'),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='This sensor name is not available. Available sensors: H2S_1, H2S_2, PM10_1, PM10_2'),
        },
    )
    def post(self, request):
        """Configure a sensor to be queried by the system, this is the only endpoint to add sensors"""
        serializer = SensorSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data.get('name') not in available_sensors:
                return Response('This sensor name is not available. Available sensors: H2S_1, H2S_2, PM10_1, PM10_2',
                                status=status.HTTP_400_BAD_REQUEST)

            sensor_obj = serializer.save()
            response_data = SensorSerializer(sensor_obj).data
            return Response({"data": response_data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
