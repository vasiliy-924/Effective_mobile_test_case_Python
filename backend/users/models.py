from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from users_backend.constants import (
    EMAIL_MAX_LENGTH,
    STR_REPRESENTATION_MAX_LENGTH,
    USER_FIELD_MAX_LENGTH,
)
from users.validators import validate_username_value


class User(AbstractUser):
    """The user's model."""

    class Roles(models.TextChoices):
        """User roles."""

        ADMIN = "admin", "Админ"
        MANAGER = "manager", "Менеджер"
        USER = "user", "Пользователь"
        GUEST = "guest", "Гость"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name")

    first_name = models.CharField(
        verbose_name="имя",
        max_length=USER_FIELD_MAX_LENGTH
    )
    last_name = models.CharField(
        verbose_name="фамилия",
        max_length=USER_FIELD_MAX_LENGTH
    )
    patronymic = models.CharField(
        verbose_name="отчество",
        max_length=USER_FIELD_MAX_LENGTH
    )
    email = models.EmailField(
        verbose_name="email адрес",
        max_length=EMAIL_MAX_LENGTH,
        unique=True
    )
    role = models.CharField(
        verbose_name="роль",
        max_length=max(len(role) for role, _ in Roles.choices),
        choices=Roles.choices,
        default=Roles.GUEST,
    )
    is_active = models.BooleanField(
        verbose_name="Активный",
        default=True
    )
    # Optional models
    username = models.CharField(
        verbose_name="никнейм",
        max_length=USER_FIELD_MAX_LENGTH,
        unique=True,
        help_text=(
            f"Обязательно. Не более {USER_FIELD_MAX_LENGTH} символов. "
            f"Только буквы, цифры и @/./+/-/_. "
        ),
        validators=(validate_username_value,)
    )
    avatar = models.ImageField(
        verbose_name="аватар пользователя",
        blank=True
    )

    class Meta:
        """Meta options for User model."""
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    def __str__(self) -> str:
        """String representation of the user."""
        return str(self.username)[:STR_REPRESENTATION_MAX_LENGTH]
