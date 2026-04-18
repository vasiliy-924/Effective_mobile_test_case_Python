from django.apps import AppConfig


class UsersConfig(AppConfig):
    """User application settings."""

    default_auto_field = "django.db.models.AutoField"
    name = 'users'
    verbose_name = "Пользователи"
