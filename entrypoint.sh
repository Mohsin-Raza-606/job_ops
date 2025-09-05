#!/usr/bin/env bash
set -e

if [ -n "$DB_HOST" ]; then
  echo "Waiting for database..."
  until nc -z "$DB_HOST" "${DB_PORT:-5432}"; do
    sleep 1
  done
  echo "Database ready."
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Starting gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
