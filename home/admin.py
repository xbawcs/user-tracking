from django.contrib import admin
from django.apps import apps
from home import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Base read only model
class BaseReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# User Tracking -------------------
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ('code', 'name')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "token")
    search_fields = ('user__username', 'code', 'token')


class DeviceLogAdmin(BaseReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("device", "type", "application", "message", "image")
    search_fields = ('device__code', 'type', 'application__code')
    list_filter = ('type', 'application')


class DeviceActivityAdmin(BaseReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("created_by", "device", "type", "log", "created_at")
    search_fields = ('device__code', 'type')
    list_filter = ('type',)
    
admin.site.register(models.Application, ApplicationAdmin)
admin.site.register(models.Device, DeviceAdmin)
admin.site.register(models.DeviceLog, DeviceLogAdmin)
admin.site.register(models.DeviceActivity, DeviceActivityAdmin)

# END: User Tracking--------------------------

# Auth User ----------------------------
class AccountInline(admin.StackedInline):
    model = models.Account
    can_delete = False
    verbose_name_plural = "account"

class UserAdmin(BaseUserAdmin):
    inlines = [AccountInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# END: Auth User ----------------------------
