import pytest
from rest_framework import status


def _access_token(client, email, password):
    response = client.post(
        "/api/auth/login/",
        {"email": email, "password": password},
        format="json",
    )
    return response.data["tokens"]["access"]


@pytest.mark.django_db
def test_rules_api_forbidden_for_non_admin(
    api_client,
    regular_user,
    rbac_catalog,
    issue_rule,
):
    issue_rule("user", "book", read_all_permission=True)
    token = _access_token(api_client, "user@test.local", "UserPassword123!")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = api_client.get("/api/rules/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_rules_api_allowed_for_admin(
    api_client,
    admin_user,
    rbac_catalog,
):
    token = _access_token(api_client, "admin@test.local", "AdminPassword123!")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    create_response = api_client.post(
        "/api/rules/",
        {
            "role": "manager",
            "element": "rules",
            "read_permission": True,
            "read_all_permission": True,
            "create_permission": False,
            "update_permission": False,
            "update_all_permission": False,
            "delete_permission": False,
            "delete_all_permission": False,
        },
        format="json",
    )
    assert create_response.status_code == status.HTTP_201_CREATED

    list_response = api_client.get("/api/rules/")
    assert list_response.status_code == status.HTTP_200_OK
    assert list_response.data["count"] >= 1
