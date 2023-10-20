# VaultMaster Backend

## DB setup guide
- Start the database container by running the following command.
```sh
docker compose up -d database
```
- Enable migration by running the following command
```sh
docker compose run backend alembic revision --autogenerate -m "MESSAGE"
```
- Upgrade the head by running the following command
```sh
docker compose run backend albmeic upgrade head
```