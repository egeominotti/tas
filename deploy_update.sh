#!/bin/bash
source venv/bin/activate
git pull
pip3 install -r requirements.txt
python3.9 manage.py migrate --noinput
python3.9 manage.py collectstatic --noinput
systemctl restart daphne
systemctl restart nginx
systemctl restart runnerbacktesting
source venv/bin/activate
