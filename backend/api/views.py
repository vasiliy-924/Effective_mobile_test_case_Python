from http import HTTPStatus

from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from api.paginations import LimitPageNumberPagination
from api.services import build_absolute_file_url
from api.serializers import (
    SetAvatarSerializer,
    UserSerializer,
)
from users.models import User


class UsersViewSet(DjoserUserViewSet):
    """Working with users and their profiles."""

    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitPageNumberPagination

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        """Returns the current user profile data."""
        serializer = UserSerializer(
            request.user,
            context={"request": request}
        )
        return Response(serializer.data)
    
    @action(
        detail=False,
        methods=("put",),
        permission_classes=(IsAuthenticated,),
        url_path="me/avatar",
    )
    def avatar(self, request):
        """Sets the current user avatar from base64."""
        serializer = SetAvatarSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"avatar": build_absolute_file_url(request, request.user.avatar)}
        )

    @avatar.mapping.delete
    def delete_avatar(self, request):
        """Deletes the current user avatar if it is set."""
        request.user.avatar.delete(save=True)
        return Response(status=HTTPStatus.NO_CONTENT)
    
