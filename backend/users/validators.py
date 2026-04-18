import re

from rest_framework import serializers

USERNAME_REGEX = r"^[\w.@+-]+\Z"


def validate_username_value(value: str) -> str:
    """Validates username using regex."""
    if not re.fullmatch(USERNAME_REGEX, value):
        raise serializers.ValidationError(
            "Имя пользователя содержит запрещенные символы."
        )
    return value
