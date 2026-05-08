#!/bin/sh
set -e

if [ -n "$POSTGRES_HOST" ]; then
  echo "Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."
  while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
    sleep 1
  done
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput || true

exec "$@"
