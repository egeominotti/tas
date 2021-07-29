#!/bin/bash
source venv/bin/activate
git pull
pip3 install -r requirements.txt
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
systemctl restart redis
systemctl restart gunicorn
systemctl restart nginx
source venv/bin/activate
