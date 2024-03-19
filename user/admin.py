from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .models import *

# Register your models here.
class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ['email', 'username', 'is_active', 'is_staff', 'created_at', 'updated_at']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Information', {'fields': ('created_at', 'updated_at')}),
    )

admin.site.register(User, CustomUserAdmin)