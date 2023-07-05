from django.urls import path
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="Air Quality API",
        default_version='v1',
        description="Lorenzo Leopardi",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    #path('<str:data_source_name>/', views.read_data_source),
    #path('<str:data_source_name>/config', views.config_data_source),
    path('<str:sensor_name>/measurements', views.get_measurements),
    path('create', views.create_sensor),
    # path('H2S_2/config', views.H2S_2_config),
    # path('PM10_1/config', views.PM10_1_config),
    # path('PM10_2/config', views.PM10_2_config),
    #  path('H2S_1/measurements', views.H2S_1_measurements),
    #  path('H2S_2/measurements', views.H2S_2_measurements),
    #  path('PM10_1/measurements', views.PM10_1_measurements),
    #
]
