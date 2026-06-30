#!/usr/bin/env bash
set -o errexit

python manage.py repair_catalog_media --quiet || true
exec gunicorn abito_web.wsgi:application
