#!/bin/bash
python3 backend/manage.py makemigrations --no-input
python3 backend/manage.py migrate --no-input
python3 backend/manage.py createsuperuser --noinput --email $DJANGO_SUPERUSER_EMAIL --first_name $DJANGO_SUPERUSER_FIRST_NAME --last_name $DJANGO_SUPERUSER_LAST_NAME
python3 backend/manage.py runserver 0.0.0.0:$PORT
