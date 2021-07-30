#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
sleep 5

pip3 install -r requirements.txt
python3 manage.py reset_db --noinput
python3 manage.py migrate --noinput
python3 manage.py dbrestore --noinput
python3 manage.py migrate --noinput

exec "$@"
