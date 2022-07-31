#! /bin/bash

rm ./**/migrations/0*.py
rm ./*.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata data.json
