import boto3
import os

def get_db_auth() -> str:
    # Get host of DB from env (default "localhost" = running FastAPI locally, non-containerized)
    PG_HOST = os.environ.get("POSTGRES_HOST", "localhost")

    # If not running in AWS, return passwd variable from env
    if not PG_HOST.endswith("rds.amazonaws.com"):
        return os.environ["POSTGRES_PASSWORD"]
    # If on AWS, access secrets store for current token
    else:
        return _get_aws_token(PG_HOST)
    
def _get_aws_token(PG_HOST) -> str:
    PG_USER = os.environ["POSTGRES_USER"]
    PG_AWS_REGION = os.environ["PG_AWS_REGION"]
    
    session = boto3.Session(region_name=PG_AWS_REGION)
    client = session.client('rds')

    token = client.generate_db_auth_token(DBHostname=PG_HOST, Port="5432", \
                                          DBUsername=PG_USER, Region=PG_AWS_REGION)

    return token    

def get_db_url(is_alembic=False) -> str:
    # Conceal secrets in .env file
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_DB = os.environ.get("POSTGRES_DB", POSTGRES_USER)
    # Allows interop between docker-compose and local dev
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
    # Pulls AWS auth token if run in cloud; otherwise, pulls from local env
    POSTGRES_PASSWORD = get_db_auth()
    
    if is_alembic:
        POSTGRES_PASSWORD = POSTGRES_PASSWORD.replace('%', '%%')

    DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

    return DATABASE_URL