from rest_framework import serializers
from .models import Pollutant, Sensor, Measurement


class PollutantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pollutant
        fields = ['name']


class SensorSerializer(serializers.ModelSerializer):
    pollutant = PollutantSerializer(read_only=True)
    pollutant_name = serializers.CharField(write_only=True)

    class Meta:
        model = Sensor
        fields = ['name', 'pollutant', 'pollutant_name', 'min_valid', 'max_valid']

    def create(self, validated_data):
        pollutant_name = validated_data.pop('pollutant_name')
        try:
            pollutant = Pollutant.objects.get(name=pollutant_name)
        except Pollutant.DoesNotExist:
            raise serializers.ValidationError('Pollutant not found')
        validated_data['pollutant'] = pollutant
        return super().create(validated_data)


class MeasurementSerializer(serializers.ModelSerializer):
    sensor = serializers.PrimaryKeyRelatedField(queryset=Sensor.objects.all(), write_only=True, required=False)
    pollutant = serializers.PrimaryKeyRelatedField(queryset=Pollutant.objects.all(), write_only=True, required=False)
    sensor_name = serializers.SerializerMethodField()
    pollutant_name = serializers.SerializerMethodField()

    class Meta:
        model = Measurement
        fields = ['created', 'sensor', 'sensor_name', 'pollutant', 'pollutant_name', 'value', 'isValid']

    def get_sensor_name(self, obj):
        return obj.sensor.name

    def get_pollutant_name(self, obj):
        return obj.pollutant.name
