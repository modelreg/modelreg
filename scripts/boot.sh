#!/bin/bash

MANAGE="python /usr/src/app/manage.py"

# Initialize Modelreg app: Migrate, create superuser, collect static files
mkdir -p /usr/src/app/modelreg/static
$MANAGE init_modelreg

if [ -n "$UWSGI" ]; then
    uwsgi --uwsgi-socket 0.0.0.0:$PORT \
        --wsgi-file /usr/src/app/modelreg/wsgi.py
else
    $MANAGE runserver 0.0.0.0:$PORT
fi
