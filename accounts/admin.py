# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the CustomUser model.
    Extends Django's built-in UserAdmin to support additional fields like
    role, phone, and profile_image.
    """

    model = CustomUser

    # Columns displayed in the admin user list view
    list_display = ('email', 'role', 'phone', 'profile_image', 'is_active', 'is_staff')

    # Filters shown in the sidebar for quick filtering
    list_filter = ('role', 'is_active', 'is_staff')

    # Fields that can be searched using the admin search bar
    search_fields = ('email', 'phone')

    # Default ordering of the user list
    ordering = ('email',)

    # Layout of fields when editing an existing user in the admin
    fieldsets = (
        ('Account Info', {
            'fields': ('email', 'password', 'profile_image', 'phone', 'role')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login',)
        }),
    )

    # Layout of fields when creating a new user in the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'profile_image',
                'phone',
                'role',
                'is_active',
                'is_staff'
            ),
        }),
    )


# Register the CustomUser model with its custom admin configuration
admin.site.register(CustomUser, CustomUserAdmin)
