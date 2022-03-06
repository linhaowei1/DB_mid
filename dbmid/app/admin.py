from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserExtension

class UserInline(admin.StackedInline):
    model = UserExtension
    can_delete = False
    verbose_name_plural = 'User_extention'

class UserAdmin(BaseUserAdmin):
    inlines = (UserInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)