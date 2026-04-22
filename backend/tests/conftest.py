import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from users.models import AccessRoleRule, BusinessElement, Role


User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def rbac_catalog(db):
    roles = {
        code: Role.objects.get_or_create(
            code=code,
            defaults={"name": code.title()}
        )[0]
        for code in ("admin", "manager", "user", "guest")
    }
    elements = {
        code: BusinessElement.objects.get_or_create(
            code=code,
            defaults={"name": code.title()},
        )[0]
        for code in ("book", "order", "rules")
    }
    return {"roles": roles, "elements": elements}


@pytest.fixture
def admin_user(db, rbac_catalog):
    return User.objects.create_user(
        username="admin",
        email="admin@test.local",
        password="AdminPassword123!",
        first_name="Admin",
        last_name="User",
        patronymic="User",
        role=rbac_catalog["roles"]["admin"],
    )


@pytest.fixture
def regular_user(db, rbac_catalog):
    return User.objects.create_user(
        username="regular",
        email="user@test.local",
        password="UserPassword123!",
        first_name="Regular",
        last_name="User",
        patronymic="User",
        role=rbac_catalog["roles"]["user"],
    )


@pytest.fixture
def guest_user(db, rbac_catalog):
    return User.objects.create_user(
        username="guest",
        email="guest@test.local",
        password="GuestPassword123!",
        first_name="Guest",
        last_name="User",
        patronymic="User",
        role=rbac_catalog["roles"]["guest"],
    )


@pytest.fixture
def issue_rule(db):
    def _issue(role_code, element_code, **overrides):
        defaults = {
            "read_permission": False,
            "read_all_permission": False,
            "create_permission": False,
            "update_permission": False,
            "update_all_permission": False,
            "delete_permission": False,
            "delete_all_permission": False,
        }
        defaults.update(overrides)
        element = BusinessElement.objects.get(code=element_code)
        AccessRoleRule.objects.update_or_create(
            role_id=role_code,
            element=element,
            defaults=defaults,
        )

    return _issue
