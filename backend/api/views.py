from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAdminRole
from api.serializers import (
    CurrentUserSerializer,
    LoginSerializer,
    LogoutSerializer,
    RegisterSerializer,
    RuleSerializer,
    SoftDeleteSerializer,
)
from users.models import AccessRoleRule
from users.services import (
    blacklist_refresh_token,
    issue_tokens_for_user,
    soft_delete_user,
)


class RegisterView(APIView):
    """Create a new user account."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = issue_tokens_for_user(user)
        return Response(
            {
                "user": CurrentUserSerializer(
                    user,
                    context={"request": request},
                ).data,
                "tokens": tokens,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """Authenticate user and issue a JWT pair."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response(
            {
                "user": CurrentUserSerializer(
                    user,
                    context={"request": request},
                ).data,
                "tokens": issue_tokens_for_user(user),
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """Invalidate a refresh token."""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        blacklist_refresh_token(serializer.validated_data["refresh"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class CurrentUserView(APIView):
    """Read and update the current authenticated user profile."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(
            CurrentUserSerializer(
                request.user,
                context={"request": request},
            ).data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request):
        serializer = CurrentUserSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CurrentUserDeleteView(APIView):
    """Soft-delete the current user account."""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = SoftDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        soft_delete_user(request.user)
        refresh = serializer.validated_data.get("refresh")
        if refresh:
            blacklist_refresh_token(refresh)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RuleViewSet(viewsets.ModelViewSet):
    """Admin-only CRUD API for RBAC rules."""

    queryset = AccessRoleRule.objects.select_related(
        "role", "element"
    ).order_by("id")
    serializer_class = RuleSerializer
    permission_classes = (IsAuthenticated, IsAdminRole)
