#miniproject/ecotrack/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the CustomUser model.
    Extends Django's built-in UserAdmin to support additional fields
    like role, phone, and profile_image.
    """
    model = CustomUser
    # Columns displayed in the admin user list view
    list_display = ("email", "full_name", "role","phone", "is_active", "is_staff", "date_joined")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("email", "phone", "full_name")
    ordering = ("-date_joined",)
    # Layout of fields when editing an existing user in the admin
    fieldsets = (
        (_("Account Info"), {"fields": ("email", "full_name", "profile_image", "phone", "role")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = ("email", "password")
    # Layout of fields when creating a new user in the admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email","full_name","password1","password2","profile_image","phone","role","is_active","is_staff",
            ),
        }),
    )
