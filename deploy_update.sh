#!/bin/bash
source venv/bin/activate
git pull
pip3 install -r requirements.txt
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
systemctl restart mongod
systemctl restart gunicorn
systemctl restart qcluster
systemctl restart dispatcherbot
systemctl restart websocketstream
source venv/bin/activate
