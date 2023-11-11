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


def test_vault_get_401():
    response = client.get("/vaultmaster/vault/")
    assert response.status_code == 401


def test_vault_put_401():
    response = client.put("/vaultmaster/vault")
    assert response.status_code == 401


def test_open_vault_put_401():
    response = client.put("/vaultmaster/vault/open")
    assert response.status_code == 401


def test_credential_get_401():
    response = client.get("/vaultmaster/credential/")
    assert response.status_code == 401


def test_credential_post_401():
    response = client.post("/vaultmaster/credential/")
    assert response.status_code == 401


def test_credential_put_401():
    response = client.put("/vaultmaster/credential/4354-34234")
    assert response.status_code == 401


def test_credential_delete_401():
    response = client.delete("/vaultmaster/credential/5614-ddfds2")
    assert response.status_code == 401
