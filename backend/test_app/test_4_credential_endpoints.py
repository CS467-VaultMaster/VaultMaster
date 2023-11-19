import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_user():
    return {"username": "testuser", "password": "testpassword"}


@pytest.fixture
def mock_credential():
    return {
        "nickname": "TestCredential",
        "category": "TestCategory",
        "url": "www.example.com",
        "password": "TestPassword",
        "note": "Test Note",
    }


def test_login(client, test_user):
    # Test login endpoint.
    response = client.post("/vaultmaster/user/login", data=test_user)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert "username" in response.json()

    return response.json()["access_token"]


def test_get_credentials_empty(client, test_user):
    access_token = test_login(client, test_user)
    credential_response = client.get(
        "/vaultmaster/credential",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert credential_response.status_code == 200
    assert len(credential_response.json()) == 0


def test_create_credential(client, test_user, mock_credential):
    access_token = test_login(client, test_user)
    credential_response = client.post(
        "/vaultmaster/credential",
        json=mock_credential,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert credential_response.status_code == 200

    full_credential_response = client.get(
        "/vaultmaster/credential",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    credential_lst = full_credential_response.json()

    for credential in credential_lst:
        if credential["id"] == credential_response.json()["id"]:
            assert credential["password"] == "TestPassword"


def test_update_credential(client, test_user):
    access_token = test_login(client, test_user)
    full_credential_response = client.get(
        "/vaultmaster/credential",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    credential_id = full_credential_response.json()[0]["id"]

    credential_response = client.put(
        f"/vaultmaster/credential/{credential_id}",
        json={
            "nickname": "TestCredentialUpdate",
            "category": "TestCategory",
            "url": "www.example.com",
            "password": "TestPasswordUpdate",
            "note": "Test Note",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert credential_response.status_code == 200
    assert credential_response.json()[0]["password"] == "TestPasswordUpdate"


def test_delete_credential(client, test_user):
    access_token = test_login(client, test_user)
    full_credential_response = client.get(
        "/vaultmaster/credential",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    credential_id = full_credential_response.json()[0]["id"]

    credential_response = client.delete(
        f"/vaultmaster/credential/{credential_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert credential_response.status_code == 204

    full_credential_response = client.get(
        "/vaultmaster/credential",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert len(full_credential_response.json()) == 0
