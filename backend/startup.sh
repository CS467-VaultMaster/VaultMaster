#!/bin/bash

if [ -z "$PG_AWS_REGION" ]; then
    alembic stamp head
    alembic revision --autogenerate -m "Migration message"
    alembic upgrade head
fi

# Start the application
uvicorn main:app --host 0.0.0.0 --port 8000 --reload