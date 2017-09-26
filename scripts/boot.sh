#!/bin/bash

MANAGE="python /usr/src/app/manage.py"

if [ -n "$COLLECTSTATIC" ]; then
    echo "Before collecting static, cleaning up old remains (if any)"
    rm -rfv  /usr/src/app/static/*
    mkdir -p /usr/src/app/static
fi

# Initialize Modelreg app: Migrate, create superuser, collect static files
$MANAGE init_modelreg

if [ -n "$UWSGI" ]; then
    uwsgi --uwsgi-socket 0.0.0.0:$PORT \
        --wsgi-file /usr/src/app/modelreg/wsgi.py
else
    $MANAGE runserver 0.0.0.0:$PORT
fi
