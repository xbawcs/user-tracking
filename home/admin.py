from django.contrib import admin
from django.apps import apps
from home import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User




class BaseReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# Register your models here.

# User Tracking

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("code", "name")


class DeviceAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "name", "token")


class DeviceLogAdmin(BaseReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("type", "message", "image")
    
admin.site.register(models.Application, ApplicationAdmin)
admin.site.register(models.Device, DeviceAdmin)
admin.site.register(models.DeviceLog, DeviceLogAdmin)

# Auth User
class AccountInline(admin.StackedInline):
    model = models.Account
    can_delete = False
    verbose_name_plural = "account"

class UserAdmin(BaseUserAdmin):
    inlines = [AccountInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)