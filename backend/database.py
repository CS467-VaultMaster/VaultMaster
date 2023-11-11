from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Pull Postgres credentials and configuration
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_DB = os.environ.get("POSTGRES_DB", POSTGRES_USER)
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "")
POSTGRES_ENGINE = os.environ.get("POSTGRES_ENGINE", "postgresql+psycopg2")
AWS_REGION = os.environ.get("PG_AWS_REGION", "")
SSL_MODE = os.environ.get("PG_SSLMODE", "allow")

# Build connection URL string
DATABASE_URL = f"{POSTGRES_ENGINE}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
if AWS_REGION:
    DATABASE_URL += f"?aws_region_name={AWS_REGION}&rds_sslrootcert=True&sslmode={SSL_MODE}"

engine = create_engine(DATABASE_URL)
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
