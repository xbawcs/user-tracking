from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from .models import *
from core.utils import set_pagination

# @login_required
def index(request):

  context = {
    'segment'  : 'index',

  }
  # return render(request, "pages/firebase.html", context)

  return redirect("/device/my-log")
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

def update_user(request):
    if request.method!="POST":
        messages.error(request,"Failed to update Profile")
        return HttpResponseRedirect(reverse("profile"))
    else:
        try:
            # Check email
            email = request.POST.get("email", '')
            if email and request.user.email != email and User.objects.filter(email=email).exists():
              messages.error(request, "Email already exists")
            else:
              account = Account.objects.get(user_id=request.user.id)
              account.user.first_name = request.POST.get("first_name", '')
              account.user.last_name = request.POST.get("last_name", '')
              account.user.email = request.POST.get("email", '')
              account.birthday = request.POST.get("birthday", '')
              account.bio = request.POST.get("bio", '')
              account.gender = request.POST.get("gender", '')
              account.user.save()
              account.save()
              messages.success(request,"Successfully update Profile")
        except:
            messages.error(request,"Failed to update Profile")
        return HttpResponseRedirect(reverse("profile"))