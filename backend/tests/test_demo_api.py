import pytest
from rest_framework import status


def _login(client, email, password):
    response = client.post(
        "/api/auth/login/",
        {"email": email, "password": password},
        format="json",
    )
    return response.data["tokens"]["access"]


@pytest.mark.django_db
def test_demo_books_requires_auth(api_client):
    response = api_client.get("/api/demo/books/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_demo_books_forbidden_without_rule(api_client, regular_user):
    # Override seeded rule so this scenario explicitly checks 403.
    from users.models import AccessRoleRule
    AccessRoleRule.objects.filter(role_id="user", element__code="book").update(
        read_permission=False,
        read_all_permission=False,
    )
    access = _login(api_client, "user@test.local", "UserPassword123!")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    response = api_client.get("/api/demo/books/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_demo_books_allowed_with_rule(api_client, regular_user, issue_rule):
    issue_rule("user", "book", read_all_permission=True)
    access = _login(api_client, "user@test.local", "UserPassword123!")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    response = api_client.get("/api/demo/books/")
    assert response.status_code == status.HTTP_200_OK
