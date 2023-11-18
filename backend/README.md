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

#### User

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

#### Vault

| **Field**           | **Type**    |
|---------------------|-------------|
| id (PK)             | VARCHAR     |
| credential (FK)     | VARCHAR     |
| vault_name          | VARCHAR     |
| created             | TIMESTAMPTZ |
| modified            | TIMESTAMPTZ |

#### Credential

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

#### User

**POST /register**
- This endpoint is used by users to register.
- Users can create an account by providing a username, password, first name, last name, and email.
- Upon successful registration, the endpoint will return a URI that will be used to generate a QR code for multi-factor authentication.

**POST /login**
- This endpoint is used by users to log in.
- Users will enter their login credentials (username and password) to receive a JWT token that expires after 10 minutes.
- This endpoint keeps track of how many times the user attempted to log in. After 3 consecutive failed login attempts, the user account is locked for 10 minutes.

**GET /otp_verify/{code}**
- This endpoint is used by users for multi-factor authentication when logging in.
- After a successful login using a username and password/receiving a JWT token, users will be prompted to enter a 6-digit MFA code.
- The MFA code must be verified for users to be fully authenticated.

**GET /account**
- This endpoint returns user information for the currently logged-in user.

**PUT /account**
- This endpoint is used by users to update their account information.
- Users can update their username, password, first name, last name, and email.

**DELETE /account**
- This endpoint is used by users to remove their account.

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