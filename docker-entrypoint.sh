#!/bin/sh

echo 'migrating the data base'
python manage.py migrate

echo 'running web server'
python manage.py runserver 0.0.0.0:8000