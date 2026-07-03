#!/bin/bash
set -e

echo "Waiting for MySQL..."
while ! nc -z ${DB_HOST:-mysql} ${DB_PORT:-3306}; do
    sleep 2
done

echo "Waiting for Redis..."
while ! nc -z ${REDIS_HOST:-redis} ${REDIS_PORT:-6379}; do
    sleep 2
done

echo "Running database migrations..."
flask db upgrade

echo "Starting Flask with debugpy on port 5678..."
exec python -m debugpy --listen 0.0.0.0:5678 --wait-for-client \
    -m flask run --host=0.0.0.0 --port=5000
