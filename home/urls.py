from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
  path(''       , views.index,  name='index'),
  # path('tables/', views.tables, name='tables'),
  path('device/my-log', views.device_log, name='device_log'),
  path('device/capture-screen', views.capture_screen, name='capture_screen'),
  path('device/get-location', views.get_location, name='get_location'),
  path('device/optimize-battery', views.optimize_battery, name='optimize_battery'),
  path('user/update', views.update_user, name='update_user'),
]
