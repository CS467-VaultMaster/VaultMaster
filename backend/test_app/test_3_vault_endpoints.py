import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_user():
    return {"username": "testuser", "password": "testpassword"}


def test_register_user(client):
    # Test user registration endpoint.
    data = {
        "username": "testuser",
        "password1": "testpassword",
        "password2": "testpassword",
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
    }
    response = client.post("/vaultmaster/user/register", json=data)
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["username"] == "testuser"


def test_login(client, test_user):
    # Test login endpoint.
    response = client.post("/vaultmaster/user/login", data=test_user)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert "username" in response.json()

    return response.json()["access_token"]


def test_get_vault(client, test_user):
    # Assuming you have a valid access token obtained from the login endpoint.
    access_token = test_login(client, test_user)

    # Test get vault endpoint with authentication.
    vault_response = client.get(
        "/vaultmaster/vault", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert vault_response.status_code == 200
    user_response = client.get(
        "/vaultmaster/user/account", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert user_response.status_code == 200
    vault_json = vault_response.json()
    user_json = user_response.json()
    # User id associated with the vault should match the token bearer.
    assert vault_json["user_id"] == user_json["id"]


def test_update_vault(client, test_user):
    # Assuming you have a valid access token obtained from the login endpoint.
    access_token = test_login(client, test_user)
    data = {"vault_name": "UpdatedVaultName"}
    vault_response = client.put(
        "/vaultmaster/vault",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert vault_response.json()["vault_name"] == "UpdatedVaultName"


def test_open_vault(client, test_user):
    # Assuming you have a valid access token obtained from the login endpoint.
    access_token = test_login(client, test_user)
    data = {"password": "testpassword"}
    vault_response = client.put(
        "/vaultmaster/vault/open",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert vault_response.status_code == 200


def test_open_vault_incorrect_password(client, test_user):
    # Assuming you have a valid access token obtained from the login endpoint.
    access_token = test_login(client, test_user)
    data = {"password": "testpassword1"}
    vault_response = client.put(
        "/vaultmaster/vault/open",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert vault_response.status_code == 401
