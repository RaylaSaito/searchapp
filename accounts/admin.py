from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('account_id', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'birth_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('account_id', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('account_id', 'email', 'is_staff', 'is_active')
    search_fields = ('account_id', 'email')
    ordering = ('account_id',)

admin.site.register(User, UserAdmin)
