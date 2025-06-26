"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models

class UserAdmin(BaseUserAdmin):
    """Define admin pages for user."""
    order = ['id']
    list_display = ['name, email']


admin.site.register(models.User, UserAdmin)
    
