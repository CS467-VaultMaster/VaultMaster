# VaultMaster Backend
This repository houses the backend for VaultMaster, developed using [FastAPI](https://fastapi.tiangolo.com/) and [PostgreSQL](https://www.postgresql.org/). It facilitates user interaction with the application, including registration, login, logout, and CRUD operations on user profiles, vaults, and web credentials.

## Technologies
- [Python](https://www.python.org/)
- [Go](https://go.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)/[Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Passlib](https://github.com/glic3rinu/passlib)
- [python-jose](https://github.com/mpdavis/python-jose/tree/master)
- [cryptography](https://github.com/pyca/cryptography)

## Data Models

## APIs

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