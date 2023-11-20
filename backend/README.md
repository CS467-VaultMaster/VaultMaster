# VaultMaster Backend
This repository houses the backend for VaultMaster, developed using [FastAPI](https://fastapi.tiangolo.com/) and [PostgreSQL](https://www.postgresql.org/). It facilitates user interaction with the application, including registration, login, logout, and CRUD operations on user profiles, vaults, and web credentials.

## Technologies
- [Python](https://www.python.org/)
- [Go](https://go.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/) and [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Passlib](https://github.com/glic3rinu/passlib)
- [python-jose](https://github.com/mpdavis/python-jose/tree/master)
- [cryptography](https://github.com/pyca/cryptography)

## Data Models

### User :sunglasses:

| **Field**           | **Type**    |
|---------------------|-------------|
| id (PK)             | VARCHAR     |
| vault (FK)          | VARCHAR     |
| username            | VARCHAR     |
| password            | VARCHAR     |
| email               | VARCHAR     |
| first_name          | VARCHAR     |
| last_name           | VARCHAR     |
| created             | TIMESTAMPTZ |
| modified            | TIMESTAMPTZ |
| last_verified       | TIMESTAMPTZ |
| last_login_attempt  | TIMESTAMPTZ |
| login_attempts      | SMALLINT    |

### Vault :shield:

| **Field**           | **Type**    |
|---------------------|-------------|
| id (PK)             | VARCHAR     |
| credential (FK)     | VARCHAR     |
| vault_name          | VARCHAR     |
| created             | TIMESTAMPTZ |
| modified            | TIMESTAMPTZ |

### Credential :closed_lock_with_key:

| **Field**           | **Type**    |
|---------------------|-------------|
| id (PK)             | VARCHAR     |
| nickname            | VARCHAR     |
| category            | VARCHAR     |
| url                 | VARCHAR     |
| password            | VARCHAR     |
| note                | VARCHAR     |
| created             | TIMESTAMPTZ |
| modified            | TIMESTAMPTZ |
| fernet_key          | TIMESTAMPTZ |

## APIs

### User :sunglasses:

**POST /vaultmaster/user/register**
- This endpoint is used for user registration.
- Users can create an account by providing a username, password, first name, last name, and email.
- Upon successful registration, the endpoint returns a URI, which is used to generate a QR code for multi-factor authentication.

**POST /vaultmaster/user/login**
- This endpoint is used for user login.
- Users enter their login credentials (username and password) to receive a JWT token that expires after 10 minutes.
- The endpoint tracks login attempts, and after 3 consecutive failed login attempts, the user account is locked for 10 minutes.

**GET /vaultmaster/user/otp_verify/{code}**
- This endpoint is used for multi-factor authentication during login.
- After a successful login (using a username + password and receiving a JWT token), users are prompted to enter a 6-digit MFA code.
- The MFA code must be verified for full user authentication.

**GET /vaultmaster/user/account**
- This endpoint returns user information for the currently logged-in user.

**PUT /vaultmaster/user/account**
- This endpoint is used for updating user account information.
- Users can update their username, password, first name, last name, and email.

**DELETE /vaultmaster/user/account**
- This endpoint is used for removing a user account.

### Vault :shield:

**GET /vaultmaster/vault**
- This endpoint retrieves the vault assigned to the currently logged-in user.

**PUT /vaultmaster/vault**
- This endpoint is used for updating the user's vault.
- Only the vault name can be updated.

**PUT /vaultmaster/vault/open**
- This endpoint is used for opening the assigned vault.
- Users are required to enter their master password (same as their login password) to open the vault and access their web credentials.

### Credential :closed_lock_with_key:

**GET /vaultmaster/credential**
- This endpoint returns the list of web credentials in the currently logged-in user's vault.

**POST /vaultmaster/credential**
- This endpoint is used for adding a new web credential to the vault.
- Users can enter a nickname, category, URL, password, and note for the credential they want to store.

**PUT /vaultmaster/credential/{credential_id}**
- This endpoint is used for updating a web credential in the vault.
- Users can update the nickname, category, URL, password, and note of the credential.

**DELETE /vaultmaster/credential/{credential_id}**
- This endpoint is used for deleting a web credential from the vault.


## Encryption and Decryption
<!---
## DB setup guide
- Start the database container by running the following command.
```sh
docker compose up -d database
```
- Stamp the head
```sh
docker compose run backend alembic stamp head
```
- Enable migration by running the following command
```sh
docker compose run backend alembic revision --autogenerate -m "MESSAGE"
```
- Upgrade the head by running the following command
```sh
docker compose run backend alembic upgrade head
```
- Start the rest of the docker-compose.
```sh
docker compose up -d
```
- Navigate to the following to test out the backend APIs.
```sh
localhost:8000/docs
```
--->