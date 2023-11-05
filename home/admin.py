from django.contrib import admin
from django.apps import apps
from home import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import gettext as _
admin.ModelAdmin.list_per_page = settings.LIST_PER_PAGE

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
    readonly_fields = ["user", 'code']
    list_display = ("user", "code", 'name', "token")
    exclude = ('is_interval',)
    search_fields = ('user__username', 'code', 'is_interval', 'token')

    change_form_template = "pages/change_form.html"

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        show_loop_capture = False
        if obj and not obj.is_interval:
            show_loop_capture = True
        context.update({'show_loop_capture': show_loop_capture})
        return super().render_change_form(request, context, add, change, form_url, obj)

    def response_change(self, request, obj):
        if "_stop-loop-capture" in request.POST:
            if obj:
                obj.loop_capture(not obj.is_interval)
                # self.message_user(request, "Loop capture disabled")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)  


class DeviceLogAdmin(BaseReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("device", "type", "application", "message", "image", "created_at")
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
