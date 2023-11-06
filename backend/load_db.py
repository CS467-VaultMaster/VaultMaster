import psycopg2
import os
from db_auth import get_db_auth


def load_db(path: str) -> bool:
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_DB = os.environ.get("POSTGRES_DB", POSTGRES_USER)
    # Allows interop between docker-compose and local dev
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
    # Pulls AWS auth token if run in cloud; otherwise, pulls from local env
    POSTGRES_PASSWORD = get_db_auth()
    PG_SSLCERT = os.environ["PG_SSLCERT"]

    try: 
        conn = psycopg2.connect(host=POSTGRES_HOST, 
                                port="5432", 
                                database=POSTGRES_DB,
                                user=POSTGRES_USER,
                                pasword=POSTGRES_PASSWORD,
                                sslrootcert=PG_SSLCERT)
        
        cursor = conn.cursor()
    except Exception as e:
        print(e)
        return

    with open(path, 'r') as f:
        cursor.execute(f.read())
        cursor.close()
    
    conn.close()
