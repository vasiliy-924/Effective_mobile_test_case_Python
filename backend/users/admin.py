from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import AccessRoleRule, BusinessElement, Role, User


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin panel for role management."""

    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(BusinessElement)
class BusinessElementAdmin(admin.ModelAdmin):
    """Admin panel for business elements."""

    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(AccessRoleRule)
class AccessRoleRuleAdmin(admin.ModelAdmin):
    """Admin panel for access rules."""

    list_display = (
        "role",
        "element",
        "read_permission",
        "read_all_permission",
        "create_permission",
        "update_permission",
        "update_all_permission",
        "delete_permission",
        "delete_all_permission",
    )
    list_filter = ("role", "element")
    search_fields = ("role__code", "role__name", "element__code", "element__name")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin panel for the User model."""

    list_display = (
        "first_name",
        "last_name",
        "patronymic",
        "email",
        "username",
        "role",
        "avatar"
    )
    list_display_links = ("username", "email")
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name", 
        "patronymic",
        "role__code",
        "role__name",
    )
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            'Дополнительно',
            {
                'fields': (
                    'role',
                    'avatar',
                )
            }
        ),
    )
