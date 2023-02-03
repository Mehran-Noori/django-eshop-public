#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input --clear --verbosity=0

DJANGO_SUPERUSER_PASSWORD=password python manage.py createsuperuser --username username --email name@test.com --no-input

python manage.py runserver 0.0.0.0:8000

exec "$@"
