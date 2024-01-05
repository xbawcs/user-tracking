from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from .models import *
from core.utils import set_pagination
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from firebase_admin import credentials, messaging
from django.utils.translation import gettext_lazy as _
from admin_datta.views import UserLoginView

# Custom auth
class CustomAuthToken(ObtainAuthToken):

  def post(self, request, *args, **kwargs):
      if request.data and not request.data.get('device_token', ''):
        return Response({'device_token': _('"device_token" must be required')})

      serializer = self.serializer_class(data=request.data,
                                          context={'request': request})
      serializer.is_valid(raise_exception=True)
      user = serializer.validated_data['user']
      token, created = Token.objects.get_or_create(user=user)
      # Get device or create
      device, created = Device.objects.get_or_create(user=user)
      device.token = request.data.get('device_token')
      device.save()

      return Response({
          'token': token.key,
          'device': device.code
      })
  
UserLoginView.template_name = 'pages/auth-signin.html'

# END: Custom auth ------------

@login_required
def index(request):

  context = {
    'segment'  : 'index',

  }
  if not request.user.is_superuser:
    return HttpResponseRedirect(reverse("device_log"))
  else:
    return render(request, "pages/profile.html", context)

@login_required
def tables(request):
  context = {
    'segment': 'tables'
  }
  return render(request, "pages/dynamic-tables.html", context)

# --------- Device action -----------
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
  device = Device.objects.filter(user_id=user.id).first()
  device_ids = [device.id] if device else []
  context['loop_capture'] = device.is_interval if device else False
  if device_ids:
    device_log = DeviceLog.objects.filter(device__in=device_ids, ignore=False).order_by('-created_at')
    context['transactions'], context['info'] = set_pagination(request, device_log, settings.LIST_PER_PAGE)

  return render(request, "home/device_log.html", context)

@login_required
def delete_log(request):
  if request.method!="POST":
    messages.error(request, 'Method not allowed.')
    return HttpResponseRedirect(reverse("device_log"))
  else:
    context = {
      'segment': 'delete_log'
    }
    log_ids = [eval(i) for i in request.POST.getlist("selected_options")] \
                    if request.POST.getlist("selected_options") else []
    if log_ids:
      device = Device.objects.filter(user_id=request.user.id).first()
      device_log = DeviceLog.objects.filter(id__in=log_ids)
      if device_log:
        error = ''
        for dl in device_log:
          if dl.device != device:
              error = _('You cannot delete records that are not yours')
              break
      else:
        error = _('You cannot delete records that are not yours')
    else:
      error = _('Please select records to delete')
    if error:
      messages.error(request, error)
    else:
      device_log.delete()
      messages.success(request, _("Records has been deleted successfully"))
    return HttpResponseRedirect(reverse("device_log"))

@login_required
def capture_screen(request):
  if request.method!="POST":
    messages.error(request, 'Method not allowed.')
    return HttpResponseRedirect(reverse("device_log"))
  else:
    user = request.user
    device = Device.objects.filter(user_id=user.id).first()
    error = ''
    if not device:
      error = _('Unsuccessful because user does not have any devices.')
    else:
      if device.token:
        device.capture_screen()
      else:
        error = _('Invalid device token.')
    # Save log action
    if error:
      log = error
      messages.error(request, error)
    else:
      log = _("Request has been sent successfully")
      messages.success(request, log)
    DeviceActivity(created_by= user, device=device if device else None, type='capture', log=log).save()
    return HttpResponseRedirect(reverse("device_log"))
  
@login_required
def get_location(request):
  if request.method!="POST":
    messages.error(request, _('Method not allowed.'))
    return HttpResponseRedirect(reverse("device_log"))
  else:
    user = request.user
    device = Device.objects.filter(user_id=user.id).first()
    error = ''
    if not device:
      error = _('Unsuccessful because user does not have any devices.')
    else:
      if device.token:
        device.get_location()
      else:
        error = _('Invalid device token.')
    # Save log action
    if error:
      log = error
      messages.error(request, error)
    else:
      log = _("Request has been sent successfully")
      messages.success(request, log)
    DeviceActivity(created_by= user, device=device if device else None, type='location', log=log).save()
    return HttpResponseRedirect(reverse("device_log"))

@login_required
def optimize_battery(request):
  if request.method!="POST":
    messages.error(request, _('Method not allowed.'))
    return HttpResponseRedirect(reverse("device_log"))
  else:
    user = request.user
    device = Device.objects.filter(user_id=user.id).first()
    error = ''
    if not device:
      error = _('Unsuccessful because user does not have any devices.')
    else:
      if device.token:
        device.optimize_battery()
      else:
        error = _('Invalid device token.')
    # Save log action
    if error:
      log = error
      messages.error(request, error)
    else:
      log = _("Request has been sent successfully")
      messages.success(request, log)
    DeviceActivity(created_by= user, device=device if device else None, type='optimize', log=log).save()
    return HttpResponseRedirect(reverse("device_log"))


@login_required
def loop_capture(request):
  if request.method!="POST":
    messages.error(request, _('Method not allowed.'))
    return HttpResponseRedirect(reverse("device_log"))
  else:
    user = request.user
    device = Device.objects.filter(user_id=user.id).first()
    error = ''
    loop_capture = request.POST.get("loop_capture", '')
    if not device:
      error = _('Unsuccessful because user does not have any devices.')
    else:
      if device.token:
        device.loop_capture(True if loop_capture == '1' else False)
      else:
        error = _('Invalid device token.')
    # Save log action
    if error:
      log = error
      messages.error(request, error)
    else:
      if loop_capture == '1':
        log = _("[ON Capture] Request has been sent successfully")
      else:
        log = _("[OFF Capture] Request has been sent successfully")
      messages.success(request, log)
    DeviceActivity(created_by= user, device=device if device else None, type='capture_loop', log=log).save()
    return HttpResponseRedirect(reverse("device_log"))

# --------- END: Device action -----------

# --------- User action -----------
@login_required
def update_user(request):
    if request.method!="POST":
        messages.error(request, _("Failed to update profile."))
        return HttpResponseRedirect(reverse("profile"))
    else:
        try:
            # Check email
            email = request.POST.get("email", '')
            if email and request.user.email != email and User.objects.filter(email=email).exists():
              messages.error(request, _("Email already exists"))
            else:
              account, created = Account.objects.get_or_create(user=request.user)
              account.user.first_name = request.POST.get("first_name", '')
              account.user.last_name = request.POST.get("last_name", '')
              account.user.email = request.POST.get("email", '')
              account.birthday = request.POST.get("birthday") if request.POST.get("birthday") else None
              account.bio = request.POST.get("bio", '')
              account.gender = request.POST.get("gender", '')
              if request.FILES.get("avatar", None):
                account.avatar = request.FILES.get("avatar")
              account.user.save()
              account.save()
              messages.success(request, _("Successfully update profile."))
        except Exception as e:
          print('{}'.format(e))
          messages.error(request, _("Failed to update profile."))
        return HttpResponseRedirect(reverse("profile"))
    
# --------- END: User action -----------