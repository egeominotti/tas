#!/bin/bash
source venv/bin/activate
#python3 manage.py dbbackup
git pull
pip install -r requirements.txt
python3 manage.py migrate --noinput
sudo systemctl restart redis
sudo systemctl restart gunicorn
sudo systemctl restart daphne
sudo systemctl restart nginx
source venv/bin/activate
