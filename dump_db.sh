#!/bin/bash

# This script creates a dumpfile for current DB contents and schema. 
# The dumpfile can then be used to update the production server. 
# NOTE: this script is intended to be run from the project root (VaultMaster/)

# Check for .env.dev file and exit with error if not found
if [ ! -f .env.dev ]; then
    echo "ERROR: no .env.dev file found. Exiting."
    exit 1
fi

# Check for argument provided, set it to $FILENAME (or use default)
if [ -z "$1" ]; then
    filename="dump.sql"
else
    filename="$1"
fi

# Load environment variables from .env.dev
set -a 
source .env.dev
export PGPASSWORD="$POSTGRES_PASSWORD"
set +a

# Check for docker container running postgres:15.4
container_id=$(docker ps | grep "postgres:15.4" | awk '{print $1}')

# If not found, try to start up with docker compose 
if [ -z "$container_id" ]; then
    echo "No postgres container found. Starting up with docker compose..."
    docker-compose up -d database
    wait 1
    container_id=$(docker ps | grep "postgres:15.4" | awk '{print $1}')

    # if still not found, exit with error
    if [ -z "$container_id" ]; then
        echo "ERROR: could not start postgres container. Exiting."
        exit 1
    fi
fi

# Execute pg_dump command to create dumpfile
docker exec -t "$container_id" pg_dump -U "$POSTGRES_USER" -T public.alembic_version --inserts --clean --if-exists vaultmaster > "$filename"

echo "Dumpfile created: $filename"

# Check if SCP_TARGET is set (meaning user has SSH access to prod)
if [ -z "$SCP_TARGET" ]; then
    exit 0
fi

# Otherwise, upload to server
scp "$filename" "$SCP_TARGET"

# Check exit status of scp command
if [ $? -ne 0 ]; then
    echo "ERROR: scp command failed. Exiting."
    exit 1
else
    echo "Dumpfile uploaded to $SCP_TARGET"
fi

