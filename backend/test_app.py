from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# Tests for unauthorized access.
def test_user_account_get_401():
    response = client.get("/vaultmaster/user/account")
    assert response.status_code == 401


def test_user_account_put_401():
    response = client.put("/vaultmaster/user/account")
    assert response.status_code == 401


def test_user_account_delete_401():
    response = client.delete("/vaultmaster/user/account")
    assert response.status_code == 401


def test_user_otp_verify_get_401():
    response = client.get("/vaultmaster/user/otp_verify/000000")
    assert response.status_code == 401
