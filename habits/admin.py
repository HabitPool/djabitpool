from django.contrib import admin
from django import forms
from django.contrib.auth.models import User

from .models import Challenge, Sololingo, UserProfile, ProgressLog

admin.site.register(Challenge)
admin.site.register(Sololingo)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username','challenge_url','contact')  # Specify the fields you want to display in the list view
    def username(self, obj):
        return obj.user.username  # Display the username of the associated user
    def get_form(self, request, obj=None, **kwargs):
        form = super(UserProfileAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields.update({
            'contact': forms.CharField(required=False),
        })
        return form
    def save_model(self, request, obj, form, change):
        if obj.user == request.user:
            obj.save()
        else:
            super(UserProfileAdmin, self).save_model(request, obj, form, change)

admin.site.register(UserProfile, UserProfileAdmin)

class ProgressLogAdmin(admin.ModelAdmin):
    list_display = ('username', 'date')
    def username(self, obj):
        return obj.user.username  # Display the username of the associated user
    def get_form(self, request, obj=None, **kwargs):
        form = super(ProgressLogAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields.update({
            'date': forms.DateField(required=False),
            # 'challenge_url': forms.DateField(required=False),
            # Add other fields here
        })
        return form
    def save_model(self, request, obj, form, change):
        if obj.user == request.user:
            obj.save()
        else:
            super(ProgressLogAdmin, self).save_model(request, obj, form, change)

admin.site.register(ProgressLog, ProgressLogAdmin)