from django.contrib.auth.models import AbstractUser
from django.db import models

from users_backend.constants import (
    EMAIL_MAX_LENGTH,
    STR_REPRESENTATION_MAX_LENGTH,
    USER_FIELD_MAX_LENGTH,
)
from users.validators import validate_username_value


class BusinessElement(models.Model):
    """The business application object to which the rights are issued."""

    code = models.SlugField(
        verbose_name="код",
        max_length=32,
        unique=True
    )
    name = models.CharField(
        verbose_name="название",
        max_length=128
    )

    class Meta:
        verbose_name = "Элемент"
        verbose_name_plural = "Элементы"
        ordering = ("code",)

    def __str__(self) -> str:
        return str(self.name)[:STR_REPRESENTATION_MAX_LENGTH]


class Role(models.Model):
    """User role with a fixed code and display name."""

    class Codes(models.TextChoices):
        """Supported role codes."""

        ADMIN = "admin", "Админ"
        MANAGER = "manager", "Менеджер"
        USER = "user", "Пользователь"
        GUEST = "guest", "Гость"

    code = models.SlugField(
        verbose_name="код",
        max_length=max(len(code) for code, _ in Codes.choices),
        choices=Codes.choices,
        unique=True,
        default=Codes.GUEST,
    )
    name = models.CharField(
        verbose_name="название",
        max_length=128,
        unique=True,
    )

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"
        ordering = ("code",)

    def __str__(self) -> str:
        return str(self.name)[:STR_REPRESENTATION_MAX_LENGTH]


class User(AbstractUser):
    """The user's model."""

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
    role = models.ForeignKey(
        "Role",
        verbose_name="роль",
        to_field="code",
        db_column="role",
        on_delete=models.PROTECT,
        related_name="users",
        default=Role.Codes.GUEST,
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


class AccessRoleRule(models.Model):
    """Rule: role + element + permission set."""

    role = models.ForeignKey(
        "Role",
        verbose_name="роль",
        to_field="code",
        db_column="role",
        on_delete=models.CASCADE,
        related_name="access_rules"
    )
    element = models.ForeignKey(
        "BusinessElement",
        on_delete=models.CASCADE,
        related_name="access_rules",
    )

    read_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Правило доступа"
        verbose_name_plural = "Правила доступа"
        constraints = (
            models.UniqueConstraint(
                fields=("role", "element"),
                name="uniq_role_element_access_rule",
            ),
        )

    def __str__(self) -> str:
        s = f"{self.role_id}:{self.element_id}"
        return s[:STR_REPRESENTATION_MAX_LENGTH]
