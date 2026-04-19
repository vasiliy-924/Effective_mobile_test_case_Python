from typing import Final

from users.models import AccessRoleRule


HTTP_METHOD_TO_ACTION: Final[dict[str, str]] = {
    "GET": "read",
    "HEAD": "read",
    "OPTIONS": "read",
    "POST": "create",
    "PUT": "update",
    "PATCH": "update",
    "DELETE": "delete",
}


def user_has_element_access(
    user,
    element_code: str,
    action: str,
    *,
    owner_id: int | None,
) -> bool:
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
