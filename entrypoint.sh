#!/usr/bin/env bash
set -e

: "${HTTP_BIND:=0.0.0.0:9000}"
: "${DJANGO_SUPERUSER_USERNAME:=admin}"
: "${DJANGO_SUPERUSER_EMAIL:=admin@example.com}"
: "${DJANGO_SUPERUSER_PASSWORD:=admin}"
WWW_ROOT="/www"
STATIC_ROOT="${WWW_ROOT}/static"

if [ ! -f .initialized ]; then
    # https://superuser.com/a/766606
    sed -i \
        -e 's;^STATIC_ROOT\s*=.*;STATIC_ROOT = '\'"${WWW_ROOT}"\'';' \
        -e 's;^DEBUG\s*=.*;DEBUG = False;' \
        "./backend/settings.py"
    # TODO regenerate SECRET_KEY in ./backend/settings.py

    python3 manage.py collectstatic --no-input
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py createsuperuser --no-input

    touch .initialized
fi

sed -i \
    -e 's;^socket\s*=.*;http = '"${HTTP_BIND}"';' \
        -e 's;^uid\s*=.*;uid = root;' \
        -e 's;^gid\s*=.*;gid = root;' \
    ./uwsgi.ini

exec uwsgi --ini ./uwsgi.ini "$@"