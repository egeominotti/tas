#!/bin/bash
source venv/bin/activate
git pull
pip3 install -r requirements.txt
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
systemctl restart redis.service
systemctl restart gunicorn.service
systemctl restart nginx.service
source venv/bin/activate
