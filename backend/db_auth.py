import boto3
import os

def get_db_auth() -> str:
    # Get host of DB from env (default "localhost" = running FastAPI locally, non-containerized)
    PG_HOST = os.environ.get("PG_HOST", "localhost")

    # If not running in AWS, return passwd variable from env
    if not PG_HOST.endswith("rds.amazonaws.com"):
        return os.environ["POSTGRES_PASSWORD"]
    # If on AWS, access secrets store for current token
    else:
        return _get_aws_token(PG_HOST)
    
def _get_aws_token(PG_HOST) -> str:
    PG_USER = os.environ["POSTGRES_USER"]
    PG_AWS_REGION = os.environ["PG_AWS_REGION"]
    
    session = boto3.Session()
    client = session.client('rds')

    token = client.generate_db_auth_token(DBHostname=PG_HOST, Port="5432", \
                                          DBUsername=PG_USER, Region=PG_AWS_REGION)

    return token    
