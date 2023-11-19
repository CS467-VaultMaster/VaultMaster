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
def test_user2():
    return {"username": "testuser2", "password": "testpassword2"}


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


def test_register_user_with_same_username(client):
    # Test user registration endpoint with duplicate username.
    data = {
        "username": "testuser",
        "password1": "testpassword1",
        "password2": "testpassword1",
        "first_name": "Test1",
        "last_name": "User1",
        "email": "testuser1@example.com",
    }
    response = client.post("/vaultmaster/user/register", json=data)
    assert response.status_code == 409


def test_register_user_with_same_email(client):
    # Test user registration endpoint with duplicate email.
    data = {
        "username": "testuser1",
        "password1": "testpassword1",
        "password2": "testpassword1",
        "first_name": "Test1",
        "last_name": "User1",
        "email": "testuser@example.com",
    }
    response = client.post("/vaultmaster/user/register", json=data)
    assert response.status_code == 409


def test_register_user_2(client):
    # Test user registration endpoint.
    data = {
        "username": "testuser2",
        "password1": "testpassword2",
        "password2": "testpassword2",
        "first_name": "Test",
        "last_name": "User2",
        "email": "testuser2@example.com",
    }
    response = client.post("/vaultmaster/user/register", json=data)
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["username"] == "testuser2"


def test_login(client, test_user):
    # Test login endpoint.
    response = client.post("/vaultmaster/user/login", data=test_user)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert "username" in response.json()

    return response.json()["access_token"]


def test_login_with_invalid_username(client):
    # Test login endpoint with invalid username.
    test_user = {
        "username": "testuser1",
        "password": "testpassword",
    }
    response = client.post("/vaultmaster/user/login", data=test_user)
    assert response.status_code == 401


def test_login_with_incorrect_password(client):
    # Test login endpoint with incorrect password.
    test_user = {
        "username": "testuser",
        "password": "testpassword?",
    }
    response = client.post("/vaultmaster/user/login", data=test_user)
    assert response.status_code == 401


def test_login_too_many_failed_attempts(client, test_user2):
    # Test login endpoint with too many failed attempts.
    incorrect_test_user = {
        "username": "testuser2",
        "password": "test_password2",
    }
    client.post("/vaultmaster/user/login", data=incorrect_test_user)
    client.post("/vaultmaster/user/login", data=incorrect_test_user)
    # Third failed login attempt.
    client.post("/vaultmaster/user/login", data=incorrect_test_user)
    response = client.post("/vaultmaster/user/login", data=test_user2)
    assert response.status_code == 401


def test_get_user(client, test_user):
    # Assuming you have a valid access token obtained from the login endpoint.
    access_token = test_login(client, test_user)

    # Test get user endpoint with authentication.
    response = client.get(
        "/vaultmaster/user/account", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert "username" in response.json()


def test_update_user(client, test_user):
    # Assuming you have a valid access token obtained from the login endpoint.
    access_token = test_login(client, test_user)

    # Test update user endpoint with authentication.
    data = {
        "username": "testuser",
        "password1": "testpassword",
        "password2": "testpassword",
        "first_name": "Updated",
        "last_name": "User",
        "email": "testuser@example.com",
    }
    response = client.put(
        "/vaultmaster/user/account",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated"


def test_update_user_back(client, test_user):
    # Assuming you have a valid access token obtained from the login endpoint.
    access_token = test_login(client, test_user)

    # Test update user endpoint with authentication.
    data = {
        "username": "testuser",
        "password1": "testpassword",
        "password2": "testpassword",
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
    }
    response = client.put(
        "/vaultmaster/user/account",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "Test"


def test_remove_user(client, test_user):
    # Assuming you have a valid access token obtained from the login endpoint.
    access_token = test_login(client, test_user)

    # Test remove user endpoint with authentication.
    response = client.delete(
        "/vaultmaster/user/account", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 204
