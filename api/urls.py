from django.urls import re_path, path
from django.views.decorators.csrf import csrf_exempt

from api.views import *


urlpatterns = [

	path("device-log", csrf_exempt(DeviceLogView.as_view())),

]