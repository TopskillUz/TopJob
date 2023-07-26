#!/bin/bash

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for postgres..."
  while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
    sleep 0.1
  done
  echo "PostgreSQL started"
fi

poetry install
echo "Successfully installed required packages"

# create tables
alembic upgrade head

# Start server
echo "Starting server"
uvicorn app.runner:app --host 0.0.0.0 --port $SVC_PORT --reload
