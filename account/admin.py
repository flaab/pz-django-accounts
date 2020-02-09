from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models

class ProfileInline(admin.StackedInline):
    """ Stacked inline profile extending the user model to store additional user information """
    model = Profile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
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