#!/bin/sh
python3 manage.py collectstatic --noinput
gunicorn --access-logfile -  --error-logfile - -b 0.0.0.0:8000 website.wsgi 
