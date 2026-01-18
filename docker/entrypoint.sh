#!/usr/bin/env bash
set -e

echo "Waiting for DB..."
until python manage.py check --database default; do
  sleep 2
done

echo "Apply migrations..."
python manage.py migrate --noinput

echo "Collect static..."
python manage.py collectstatic --noinput || true

echo "Start server..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000
