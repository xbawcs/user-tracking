from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
import binascii
import os
from django.utils.translation import gettext as _

TYPE_LOG = (
    ('sms', _('SMS')),
    ('capture', _('Captrue screen')),
    ('location', _('Get Location')),
    ('optimize', _('Optimize Battery'))
)
GENDER = (
    ('male', _('Male')), 
    ('female', _('Female')), 
    ('unknow', _('Unknow'))
)

class Account(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday    = models.DateField(null=True, blank=True)
    gender      = models.CharField(max_length=6, choices=GENDER)
    bio         = models.TextField(null=True, blank=True)

# List of used apps 
class Application(models.Model):
    id    = models.AutoField(primary_key=True)
    code  = models.CharField(unique=True, max_length = 100) 
    name  = models.CharField(max_length = 100) 

    def __str__(self):
        return '{} - {}'.format(self.code, self.name)
    
# List of user devices 
class Device(models.Model):
    id      = models.AutoField(primary_key=True)
    code    = models.CharField(unique=True, max_length = 100) 
    name    = models.CharField(max_length = 100, null=True, blank=True) 
    token   = models.CharField(max_length = 256, null=True)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.code
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = "{}_{}".format(
                self.user.username or datetime.now().strptime('%Y%m%d%H:%M'),
                binascii.hexlify(os.urandom(3)).decode()
            )
        return super().save(*args, **kwargs)
    

# Device logs
class DeviceLog(models.Model):
    id          = models.BigAutoField(primary_key=True)
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, blank=True)
    device      = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    type        = models.CharField(max_length=8, choices=TYPE_LOG, default='sms') 
    message     = models.TextField(null=True, blank=True)
    image       = models.ImageField(null=True, blank=True, upload_to='images/')
    created_at  = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.device.code if  self.device else ''
    
# Device Actions
class DeviceActivity(models.Model):
    id          = models.BigAutoField(primary_key=True)
    device      = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True)
    type        = models.CharField(max_length=8, choices=TYPE_LOG, default='sms')
    log         = models.TextField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True, null=True)
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.device.code if  self.device else ''