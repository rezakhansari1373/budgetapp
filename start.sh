#!/usr/bin/env bash
set -o errexit

python manage.py migrate
python manage.py seed_categories
python manage.py create_admin
gunicorn budgetapp.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2
