import pytest
from rest_framework import status


@pytest.mark.django_db
def test_register_login_and_soft_delete(api_client, rbac_catalog):
    register_payload = {
        "first_name": "Vasiliy",
        "last_name": "Petrov",
        "patronymic": "Petrovich",
        "email": "vasiliy@example.com",
        "password": "StrongPassword123!",
        "re_password": "StrongPassword123!",
    }
    register_response = api_client.post(
        "/api/auth/register/",
        register_payload,
        format="json",
    )
    assert register_response.status_code == status.HTTP_201_CREATED
    assert "tokens" in register_response.data

    login_response = api_client.post(
        "/api/auth/login/",
        {
            "email": register_payload["email"],
            "password": register_payload["password"],
        },
        format="json",
    )
    assert login_response.status_code == status.HTTP_200_OK
    access = login_response.data["tokens"]["access"]
    refresh = login_response.data["tokens"]["refresh"]
    assert access
    assert refresh

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    delete_response = api_client.post(
        "/api/users/me/delete/",
        {"refresh": refresh},
        format="json",
    )
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    relogin_response = api_client.post(
        "/api/auth/login/",
        {
            "email": register_payload["email"],
            "password": register_payload["password"],
        },
        format="json",
    )
    assert relogin_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_register_rejects_password_mismatch(api_client, rbac_catalog):
    response = api_client.post(
        "/api/auth/register/",
        {
            "first_name": "Name",
            "last_name": "Surname",
            "patronymic": "Patronymic",
            "email": "mismatch@example.com",
            "password": "StrongPassword123!",
            "re_password": "AnotherPassword123!",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "re_password" in response.data
