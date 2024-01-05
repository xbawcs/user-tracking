from rest_framework import serializers
from home import models, constants
from django.conf import settings

class DeviceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeviceLog 
        fields = ['application', 'device', 'type', 'message',  'image', 'ignore']
    
    def to_internal_value(self, data):
        current_user = self.context.get('request').user
        errors = {}
        # Check application
        app = False
        if data.get('application', False):
            app = models.Application.objects.filter(code=data.get('application'))
            if not app:
                errors["application"] = ["Application'code does not exist."]
            else:
                app = app.first()
        # Check device
        device = False
        if not data.get('device', False):
            errors["device"] = ["Device'code is empty."]
        else:
            device = models.Device.objects.filter(code=data.get('device'), user=current_user.id)
            if not device:
                errors["device"] = ["Device'code does not exist or does not belong to the current user."]
            elif len(device) > 1:
                errors["device"] = ["Device'code has multiple devices."]

        # Check type
        type = data.get('type', False) 
        if type not in dict(constants.TYPE_LOG):
            errors["type"] = ["Type is not valid."]
        if errors:
            raise serializers.ValidationError({'errors': errors})
        # Check blacklist
        message = data.get('message', '')
        ignore = False
        if app.code in ('SMS', 'sms'):
            for d in settings.IGNORED_MESSAGES:
                if d in message.lower():
                    ignore = True
                    break
        values = {
            "application": app.id if app else None,
            "device": device.first().id if device else None,
            "type": type,
            "message": data.get('message', ''),
            "ignore": ignore
        }
        if data.get('image', False):
            values['image'] = data.get('image')
    
        return super().to_internal_value(values)
    
    def to_representation(self, instance):
        return instance