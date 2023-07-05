from django.urls import path
from . import views

urlpatterns = [
    path('H2S_1/', views.H2S_1_read),
    path('H2S_2/', views.H2S_2_read),
    path('PM10_1/', views.PM10_1_read),
    path('PM10_2/', views.PM10_2_read),
    path('H2S_1/config', views.H2S_1_config),
    path('H2S_2/config', views.H2S_2_config),
    path('PM10_1/config', views.PM10_1_config),
    path('PM10_2/config', views.PM10_2_config),
    ]