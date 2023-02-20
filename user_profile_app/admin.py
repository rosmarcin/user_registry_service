__author__ = "Marcin Roszczyk,"
__version__ = "0.0.1-pre-beta"
__maintainer__ = "Marcin Roszczyk"
__email__ = "mr@marcinros.net"
__status__ = "DEV"


from django.contrib import admin
from django.contrib import messages

from django import forms
from django.db.models import JSONField

from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest

from django.core.mail import send_mail

from prettyjson import PrettyJSONWidget

from user_profile_app.models import UserProfile, ProjectSettings, SoftwareProduct

from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

from import_export import resources
import requests
import json
import time

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


from user_profile_app.forms import UserCreationForm



# class UserAdmin(UserAdmin):
#     add_form = UserCreationForm
#     #add_form_template = 'admin/auth/user/add_form_mr_djb1.html'

#     #prepopulated_fields = {'username': ('first_name' , 'last_name', )}

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2','first_name', 'last_name',  ),
#         }),
#     )


# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

# UserAdmin.list_display = ('id','is_active', 'username')



class SoftwareProductAdmin(admin.ModelAdmin):
    pass

admin.site.register(SoftwareProduct, SoftwareProductAdmin)



class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)

class ProjectSettingsAdminForm(forms.ModelForm):

    EMAIL_HOST_PASSWORD = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = ProjectSettings
        fields = '__all__'


class ProjectSettingsAdmin(admin.ModelAdmin):
    form = ProjectSettingsAdminForm
    change_form_template = 'admin/mr_djb_settings_change_form.html'
    change_list_template = 'admin/mr_djb_settings_change_list.html'
    list_display = ['EMAIL_HOST',]
    list_display_links = ('EMAIL_HOST',)
    MAX_OBJECTS = 1

    def has_add_permission(self, request):
        if self.model.objects.count() >= self.MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

    def add_view(self, request, form_url='', extra_context=None):
        object_id = ProjectSettings.objects.filter().first()
        if object_id:
            return super(ProjectSettingsAdmin, self).change_view(request, str(object_id.id), form_url, extra_context)

        else:
            extra_context = extra_context or {}
            extra_context['show_save'] = True
            extra_context['show_save_and_continue'] = False
            extra_context['show_save_and_add_another'] = False
            extra_context['show_close'] = True


            return super(ProjectSettingsAdmin, self).add_view(request, form_url, extra_context)

    def changelist_view(self, request, object_id='', form_url='', extra_context=None):
        object_id = ProjectSettings.objects.filter().first()
        if object_id:
            extra_context = extra_context or {}
            extra_context['info'] =  'You are changing the mr_djb Settings'
            extra_context['show_save'] = True
            extra_context['show_save_and_continue'] = False
            extra_context['show_save_and_add_another'] = False
            #extra_context['show_close'] = True
            extra_context['show_delete'] = False

            return super(ProjectSettingsAdmin, self).change_view(request, str(object_id.id), form_url, extra_context)
        else:       
            extra_context = extra_context or {}
            #extra_context['title'] = 'Manage {}'.format(object_id)
            extra_context['info'] =  'You are creating the new mr_djb Settings'
            extra_context['show_save'] = True
            extra_context['show_save_and_continue'] = False
            extra_context['show_save_and_add_another'] = False
            extra_context['show_close'] = True

            return super(ProjectSettingsAdmin, self).add_view(request, form_url, extra_context)

    def response_change(self, request, obj):
        if "_test_mr_djb_settings" in request.POST:
            try:
                result = send_mail(
                    str(obj.email_subject),
                    str(obj.email_body),
                    str(obj.EMAIL_HOST_USER), 
                    [str(obj.approver_email),],
                    fail_silently=False,
                )

            except Exception as err:
                messages.error(request, 'Error sending test email! {}'.format(err))
                return redirect(request.path_info, request)

            messages.add_message(request, messages.SUCCESS, 'Test email send - check your mailbox')
            return redirect(request.path_info,request)
        else:
            return super().response_change(request, obj)
  

admin.site.register(ProjectSettings, ProjectSettingsAdmin)
