from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import Role
from users.services import has_element_access, method_to_action


class IsAdminRole(BasePermission):
    """Allow access only to users with admin role."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user.is_authenticated
            and user.role_id == Role.Codes.ADMIN
        )


class HasElementAccess(BasePermission):
    """Permission backed by AccessRoleRule records."""

    message = "You do not have permission for this resource."

    def has_permission(self, request, view):
        if (
            request.method in SAFE_METHODS
            and not request.user.is_authenticated
        ):
            return False
        if not request.user.is_authenticated:
            return False

        action = method_to_action(request.method)
        if action is None:
            return False

        element_code = getattr(view, "element_code", None)
        if not element_code:
            return False
        owner_id = None
        owner_getter = getattr(view, "get_owner_id", None)
        if callable(owner_getter):
            owner_id = owner_getter(request)
        return has_element_access(
            request.user,
            element_code=element_code,
            action=action,
            owner_id=owner_id,
        )
