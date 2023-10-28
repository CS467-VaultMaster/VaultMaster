import boto3
import sys
import os
import psycopg2

# TODO: add explicit typing 

######
def get_db_auth() -> str:
    # Get host of DB from env (default, localhost, is when we're running FastAPI locally and non-containerized)
    PG_HOST = os.environ.get("PG_HOST", "localhost")

    # If not running in AWS, return variable from env
    if not PG_HOST.endswith("rds.amazonaws.com"):
        return os.environ["POSTGRES_PASSWORD"]
    else:
        return _get_aws_token(PG_HOST)
    
def _get_aws_token(PG_HOST) -> str:
    PG_USER = os.environ["POSTGRES_USER"]
    #PG_DATABASE = os.environ.get("POSTGRES_DATABASE", PG_USER)
    PG_AWS_REGION = os.environ["PG_AWS_REGION"]
    #PG_SSLCERT = os.environ["PG_SSLCERT"]
    
    session = boto3.Session()
    client = session.client('rds')

    token = client.generate_db_auth_token(DBHostname=PG_HOST, Port="5432", \
                                          DBUsername=PG_USER, Region=PG_AWS_REGION)

    return token    

# Plan is to have this be the single source for all db auth; it'll check if we're runnning in AWS, and use boto to pull the RDS creds if so
# if not, it'll handle the local or in-Docker URL as needed

# Current env looks like: 
# POSTGRES_HOST = database (in container) or localhost (outside container)
# POSTGRES_USER = vaultmaster (can keep this for all)
# POSTGRES_PASSWORD = string (in local/container) or a token we get from AWSSM (in cloud)

# So we'll need tooo....
# put it all in a URL - but how do I incorporate that SSL cert? 
# chatgpt has ideas: https://chat.openai.com/c/ba41113e-350b-40e9-b158-365f8e59597b
#  - but: how do I encapsulate that "sslmode" kwarg, for localhost connections? Am I sure I even need it? 
#  - should be "verify-ca" in the container, "disable" otherwise

# Next idea: encrypt all the env stuff locally within the container, and require an IAM call to AWS to decrypt it
# - ooh I like that 
# - also, it only responds to SSH connections from *my* IP 


# But basically we have: 
# POSTGRES_USER = os.environ["POSTGRES_USER"]
# POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
# Allows interop between docker-compose and local dev
# POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")

# DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_USER}"

# will need to add SSL




#    session = boto3.session.Session()

