from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsHavePermissionOrReadOnly(BasePermission):
    """Checks permissions for ... or read only."""
    
    def has_permission(self, request, view):
        """Checks permission at the request level."""
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Checks permission at the object level."""
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
        )
