from django.urls import path
from drf_spectacular.views import SpectacularSwaggerView
from .views import PollutantAverageView, MeasurementsView, SensorCreateView



urlpatterns = [
    path('docs', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('pollutants/<str:pollutant_name>', PollutantAverageView.as_view(), name='pollutant-average'),
    path('measurements/<str:sensor_name>', MeasurementsView.as_view(), name='measurements'),
    path('configuresensor', SensorCreateView.as_view(), name='configure-sensor'),
]
