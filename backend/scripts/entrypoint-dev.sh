#!/bin/bash

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py createsuperuser --no-input --email $DJANGO_SUPERUSER_EMAIL --first_name $DJANGO_SUPERUSER_FIRST_NAME --last_name $DJANGO_SUPERUSER_LAST_NAME
python manage.py runserver 0.0.0.0:$PORT