from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Account(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday    = models.DateField(null=True, blank=True)
    gender      = models.CharField(max_length=6, choices=[('male', 'Male'), ('female', 'Female'), ('unknow', 'Unknow')])
    bio         = models.TextField(null=True, blank=True)


TYPE_LOG = (
    ('sms','SMS'),
    ('capture', 'Captrue screen'),
    ('location','Location')
)

class Application(models.Model):
    id    = models.AutoField(primary_key=True)
    code  = models.CharField(unique=True, max_length = 100) 
    name  = models.CharField(max_length = 100) 

    def __str__(self):
        return '{} - {}'.format(self.code, self.name)

class Device(models.Model):
    id    = models.AutoField(primary_key=True)
    code  = models.CharField(unique=True, max_length = 100) 
    name  = models.CharField(max_length = 100) 
    token  = models.CharField(max_length = 256, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.code, self.name)
   


class DeviceLog(models.Model):
    id    = models.BigAutoField(primary_key=True)
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, blank=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    type  = models.CharField(max_length=8, choices=TYPE_LOG, default='sms') 
    message = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.device.code 