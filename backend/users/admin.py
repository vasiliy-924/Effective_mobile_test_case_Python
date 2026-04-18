from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin panel for the User model."""

    list_display = (
        "first_name",
        "last_name",
        "patronymic",
        "email",
        "username",
        "avatar"
    )
    list_display_links = ("username", "email")
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name", 
        "patronymic"
    )
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            'Дополнительно',
            {
                'fields': (
                    'avatar',
                )
            }
        ),
    )
