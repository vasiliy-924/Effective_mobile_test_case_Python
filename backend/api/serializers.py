from djoser.serializers import UserSerializer as DjoserUserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.services import build_absolute_file_url
from users.models import User


class SetAvatarSerializer(serializers.Serializer):
    """Serializer for setting a user avatar from a base64 string."""

    avatar = Base64ImageField(required=True)

    def save(self, **kwargs):
        """Decodes base64 and saves the current user avatar."""
        user = self.context["request"].user
        avatar_file = self.validated_data["avatar"]
        user.avatar = avatar_file
        user.save(update_fields=["avatar"])
        return user
    
    def create(self, validated_data):
        """Returns validated data without creating objects."""
        return validated_data

    def update(self, instance, validated_data):
        """Does not modify the object and returns the passed instance."""
        return instance
    

class UserSerializer(DjoserUserSerializer):
    """User serializer for reading profile data."""

    avatar = serializers.SerializerMethodField()

    class Meta(DjoserUserSerializer.Meta):
        """Meta class for UserSerializer fields and read-only config."""
        model = User
        fields = (
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "username",
            "avatar"
            # don't share with is_active
        )
        read_only_fields = fields

    def get_avatar(self, obj):
        """Returns the absolute URL of the user avatar."""
        request = self.context.get('request')
        return build_absolute_file_url(request, obj.avatar)
