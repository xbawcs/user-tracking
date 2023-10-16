from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from core.utils import set_pagination

# @login_required
def index(request):

  context = {
    'segment'  : 'index',

  }
  return render(request, "pages/firebase.html", context)

  # return redirect("/device/my-log")
  # return render(request, "pages/index.html", context)

@login_required
def tables(request):
  context = {
    'segment': 'tables'
  }
  return render(request, "pages/dynamic-tables.html", context)


@login_required
def device_log(request):
  context = {
    'segment': 'device_log'
  }
  user = request.user
  page = request.GET.get('page')
  if page and page.isnumeric():
    page = int(page)
  else:
    page = 1
  devices = Device.objects.filter(user_id=user.id)
  device_ids = list(devices.values_list('id', flat=True)) if len(devices) > 0 else []
  if device_ids:
    device_log = DeviceLog.objects.filter(device__in=device_ids).order_by('-created_at')
    context['transactions'], context['info'] = set_pagination(request, device_log, 10)

  return render(request, "home/device_log.html", context)

@login_required
def capture_screen(request):
  user = request.user
  # page = request.GET.get('page')
  # if page and page.isnumeric():
  #   page = int(page)
  # else:
  #   page = 1
  # devices = Device.objects.filter(user_id=user.id)
  # device_ids = list(devices.values_list('id', flat=True)) if len(devices) > 0 else []
  # if device_ids:
  #   device_log = DeviceLog.objects.filter(device__in=device_ids).order_by('-created_at')
  #   context['transactions'], context['info'] = set_pagination(request, device_log, 10)

  return redirect("/device/my-log")

@login_required
def get_location(request):
  user = request.user
  # page = request.GET.get('page')
  # if page and page.isnumeric():
  #   page = int(page)
  # else:
  #   page = 1
  # devices = Device.objects.filter(user_id=user.id)
  # device_ids = list(devices.values_list('id', flat=True)) if len(devices) > 0 else []
  # if device_ids:
  #   device_log = DeviceLog.objects.filter(device__in=device_ids).order_by('-created_at')
  #   context['transactions'], context['info'] = set_pagination(request, device_log, 10)

  return redirect("/device/my-log")

@login_required
def optimize_battery(request):
  user = request.user
  # page = request.GET.get('page')
  # if page and page.isnumeric():
  #   page = int(page)
  # else:
  #   page = 1
  # devices = Device.objects.filter(user_id=user.id)
  # device_ids = list(devices.values_list('id', flat=True)) if len(devices) > 0 else []
  # if device_ids:
  #   device_log = DeviceLog.objects.filter(device__in=device_ids).order_by('-created_at')
  #   context['transactions'], context['info'] = set_pagination(request, device_log, 10)

  return redirect("/device/my-log")