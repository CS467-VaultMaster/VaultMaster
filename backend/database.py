from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from db_auth import get_db_auth

# Conceal secrets in .env file
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_DB = os.environ.get("POSTGRES_DB", POSTGRES_USER)
# Allows interop between docker-compose and local dev
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
# Pulls AWS auth token if run in cloud; otherwise, pulls from local env
POSTGRES_PASSWORD = get_db_auth()

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

# set up SSL certs for SQLAlchemy (only req. if running on AWS)
PG_SSLCERT = os.environ.get("PG_SSLCERT", False)
if PG_SSLCERT:
    SQLA_CONNECT_ARGS = {
        'sslmode': os.environ['PG_SSLMODE'],
        'sslcert': PG_SSLCERT
    }
else:
    SQLA_CONNECT_ARGS = {}

engine = create_engine(DATABASE_URL, connect_args=SQLA_CONNECT_ARGS)
Base = declarative_base()
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
