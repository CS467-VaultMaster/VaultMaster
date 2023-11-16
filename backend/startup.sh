#!/bin/bash

# i.e. if running locally
if [ -z "$PG_AWS_REGION" ]; then
    # Give the database a few seconds to start
    sleep 5
    
    # Apply Alembic migrations
    alembic stamp head
    alembic revision --autogenerate -m "Migration message"
    alembic upgrade head
fi

# Start the application
uvicorn main:app --host 0.0.0.0 --port 8000 --reload