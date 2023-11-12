#!/bin/bash

# This script loads a dumpfile into the production database.
# Can only be run within the host machine (on AWS). 

# Check for .env.prod file and exit with error if not found
if [ ! -f .env.prod ]; then
    echo "ERROR: no .env.prod file found. Exiting."
    exit 1
fi

# Check for argument provided, set it to $FILENAME (or use default)
if [ -z "$1" ]; then
    filename="dump.sql"
else
    filename="$1"
fi

# Load environment variables from .env.prod
set -a 
source .env.prod
set +a

# Check for running backend container (to obtain db credentials)
container_id=$(docker ps | grep "vaultmaster-backend" | awk '{print $1}')

# If not found, exit
if [ -z "$container_id" ]; then
    echo "ERROR: backend container not running."
    echo "Exiting..."
fi

# Obtain current DB credentials
db_cred=$(docker exec "$container_id" python3 db_auth.py)

# load dumpfile 
PGPASSWORD="$db_cred" psql "host=$POSTGRES_HOST port=5432 dbname=vaultmaster user=$POSTGRES_USER sslmode=$PG_SSLMODE sslrootcert=$PG_SSLROOT" -f "$filename"

# Check for success
if [ $? -ne 0 ]; then
    echo "ERROR: Unable to load dumpfile."
    exit 1
else
    echo "Dumpfile loaded to production! Have a wonderful day."
fi
