#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinpoint
python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-thread --module app.wsgi