from django.contrib import admin
from .models import Profile
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models

class ProfileInline(admin.StackedInline):
    """ Stacked inline profile extending the user model to store additional user information """
    model = Profile
    can_delete = False
    verbose_name = _('User Profile')
    verbose_name_plural = _('User Profiles')
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    """ Config class for custom user admin """
    inlines = (ProfileInline, )
    def get_inline_instances(self, request, obj=None):
        """ Return inline instances for admin, or super ones """
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# De-register user model
admin.site.unregister(User)

# Register ours instead, with our admin settings
admin.site.register(User, CustomUserAdmin)