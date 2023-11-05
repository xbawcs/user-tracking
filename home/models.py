from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
import binascii
import os
from django.utils.translation import gettext_lazy as _
from firebase_admin import credentials, messaging
from . import constants


class Account(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday    = models.DateField(null=True, blank=True, verbose_name=_("Birthday"))
    gender      = models.CharField(max_length=6, choices=constants.GENDER, verbose_name=_("Gender"))
    bio         = models.TextField(null=True, blank=True, verbose_name=_("Bio"))
    avatar      = models.ImageField(upload_to='avatar/', null=True, blank=True)

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

# List of used apps 
class Application(models.Model):
    id    = models.AutoField(primary_key=True)
    code  = models.CharField(unique=True, max_length = 100, verbose_name=_("Code")) 
    name  = models.CharField(max_length = 100, verbose_name=_("Name")) 

    class Meta:
        verbose_name = _("Application")
        verbose_name_plural = _("Applications")

    def __str__(self):
        return '{} - {}'.format(self.code, self.name)
    
# List of user devices 
class Device(models.Model):
    id              = models.AutoField(primary_key=True)
    code            = models.CharField(unique=True, max_length = 100, verbose_name=_("Code")) 
    name            = models.CharField(max_length = 100, null=True, blank=True, verbose_name=_("Name")) 
    token           = models.CharField(max_length = 256, null=True, verbose_name=_("Token"))
    user            = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    is_interval     = models.BooleanField(verbose_name=_("Loop capture"), default=False)

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")

    def __str__(self):
        return self.code
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = "{}_{}".format(
                self.user.username or datetime.now().strptime('%Y%m%d%H:%M'),
                binascii.hexlify(os.urandom(3)).decode()
            )
        return super().save(*args, **kwargs)
    
    # To send a request to capture device screen continuously
    def loop_capture(self, is_loop_capture):
        message = messaging.MulticastMessage(
          data={
            'type': '4',
            'is_interval': '1' if is_loop_capture else '0'
          },
          tokens=[self.token]
        )
        messaging.send_multicast(message)
        # Update flag loop capture
        self.is_interval = is_loop_capture
        self.save()
    
    # To send a request to capture device screen
    def capture_screen(self):
        message = messaging.MulticastMessage(
          data={'type': '1'},
          tokens=[self.token]
        )
        messaging.send_multicast(message)
    
    # To send a request to get device location
    def get_location(self):
        message = messaging.MulticastMessage(
          data={'type': '2'},
          tokens=[self.token]
        )
        messaging.send_multicast(message)

    # To send a request to optimize device battery
    def optimize_battery(self):
        message = messaging.MulticastMessage(
          data={'type': '3'},
          tokens=[self.token]
        )
        messaging.send_multicast(message)
    
    

# Device logs
class DeviceLog(models.Model):
    id          = models.BigAutoField(primary_key=True)
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Application"))
    device      = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, verbose_name=_("Device"))
    type        = models.CharField(max_length=8, choices=constants.TYPE_LOG, default='sms', verbose_name=_("Type")) 
    message     = models.TextField(null=True, blank=True, verbose_name=_("Message"))
    image       = models.ImageField(null=True, blank=True, upload_to='images/', verbose_name=_("Image"))
    created_at  = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Created at"))

    class Meta:
        verbose_name = _("Device log")
        verbose_name_plural = _("Device Logs")

    def __str__(self):
        return self.device.code if  self.device else ''
    
# Device Actions
class DeviceActivity(models.Model):
    id          = models.BigAutoField(primary_key=True)
    device      = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, verbose_name=_("Device"))
    type        = models.CharField(max_length=12, choices=constants.TYPE_ACTIVITY, default='sms', verbose_name=_("Type"))
    log         = models.TextField(null=True, blank=True, verbose_name=_("Log"))
    created_at  = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Created at"))
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name=_("Created by"))

    class Meta:
        verbose_name = _("Device activity")
        verbose_name_plural = _("Device activities")

    def __str__(self):
        return self.device.code if  self.device else ''