#!/bin/bash
source venv/bin/activate
git pull
pip install -r requirements.txt
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
sudo systemctl restart redis
sudo systemctl restart gunicorn
sudo systemctl restart nginx
source venv/bin/activate
