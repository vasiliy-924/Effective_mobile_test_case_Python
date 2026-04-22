from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from api.services import build_absolute_file_url
from users.models import AccessRoleRule, BusinessElement, Role, User
from users.services import authenticate_by_email, create_user_account


class RegisterSerializer(serializers.Serializer):
    """Register serializer with explicit password confirmation."""

    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    patronymic = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    re_password = serializers.CharField(write_only=True, min_length=8)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email already exists."
            )
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["re_password"]:
            raise serializers.ValidationError(
                {"re_password": "Passwords do not match."}
            )
        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        validated_data.pop("re_password")
        return create_user_account(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Validate login credentials."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate_by_email(
            email=attrs["email"],
            password=attrs["password"],
        )
        if user is None:
            raise serializers.ValidationError(
                {"detail": "Invalid credentials or inactive account."}
            )
        attrs["user"] = user
        return attrs


class LogoutSerializer(serializers.Serializer):
    """Refresh token payload for logout."""

    refresh = serializers.CharField()


class SoftDeleteSerializer(serializers.Serializer):
    """Optional refresh token payload for account deletion."""

    refresh = serializers.CharField(required=False)


class CurrentUserSerializer(serializers.ModelSerializer):
    """Read/update serializer for the current profile."""

    avatar = Base64ImageField(required=False, allow_null=True)
    avatar_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "avatar",
            "avatar_url",
        )
        read_only_fields = ("avatar_url",)

    def get_avatar_url(self, obj):
        request = self.context.get("request")
        return build_absolute_file_url(request, obj.avatar)


class RuleSerializer(serializers.ModelSerializer):
    """CRUD serializer for access rules."""

    role = serializers.SlugRelatedField(
        slug_field="code",
        queryset=Role.objects.all(),
    )
    element = serializers.SlugRelatedField(
        slug_field="code",
        queryset=BusinessElement.objects.all(),
    )

    class Meta:
        model = AccessRoleRule
        fields = (
            "id",
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
