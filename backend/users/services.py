from typing import Final
from uuid import uuid4

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import AccessRoleRule

User = get_user_model()

HTTP_METHOD_TO_ACTION: Final[dict[str, str]] = {
    "GET": "read",
    "HEAD": "read",
    "OPTIONS": "read",
    "POST": "create",
    "PUT": "update",
    "PATCH": "update",
    "DELETE": "delete",
}


def method_to_action(method: str) -> str | None:
    """Convert HTTP method to RBAC action."""
    return HTTP_METHOD_TO_ACTION.get(method.upper())


def has_element_access(
    user,
    element_code: str,
    action: str,
    *,
    owner_id: int | None = None,
) -> bool:
    """Check element-level access from AccessRoleRule."""
    if not user.is_authenticated:
        return False
    try:
        rule = AccessRoleRule.objects.select_related("element").get(
            role_id=user.role_id,
            element__code=element_code,
        )
    except AccessRoleRule.DoesNotExist:
        return False

    uid = user.pk

    if action == "create":
        return bool(rule.create_permission)

    if action == "read":
        if rule.read_all_permission:
            return True
        if rule.read_permission:
            return owner_id is not None and owner_id == uid
        return False

    if action == "update":
        if rule.update_all_permission:
            return True
        if rule.update_permission:
            return owner_id is not None and owner_id == uid
        return False

    if action == "delete":
        if rule.delete_all_permission:
            return True
        if rule.delete_permission:
            return owner_id is not None and owner_id == uid
        return False

    return False


def _build_username_from_email(email: str) -> str:
    base = email.split("@", 1)[0].replace(".", "_").replace("+", "_")
    suffix = uuid4().hex[:8]
    return f"{base}_{suffix}"[:150]


def create_user_account(
    *,
    first_name: str,
    last_name: str,
    patronymic: str,
    email: str,
    password: str,
):
    """Create user with generated username and default role."""
    return User.objects.create_user(
        username=_build_username_from_email(email),
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        patronymic=patronymic,
    )


def authenticate_by_email(*, email: str, password: str):
    """Authenticate by email/password."""
    return authenticate(email=email, password=password)


def issue_tokens_for_user(user) -> dict[str, str]:
    """Generate JWT access/refresh token pair for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def blacklist_refresh_token(refresh_token: str) -> None:
    """Blacklist a refresh token if possible."""
    token = RefreshToken(refresh_token)
    try:
        token.blacklist()
    except AttributeError:
        return
    except TokenError:
        return


def soft_delete_user(user) -> None:
    """Perform user soft-delete by deactivating account."""
    user.is_active = False
    user.save(update_fields=["is_active"])
