#! /bin/bash

rm **/migrations/*_initial.py
rm *.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata data.json