# VaultMaster Backend

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