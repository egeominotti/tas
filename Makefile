build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

start:
	docker-compose start

stop:
	docker-compose stop

restart:
	docker-compose stop && docker-compose start

django:
	docker exec -ti tas_developmet bash

migrate:
	docker exec -ti tas_development python3 manage.py migrate

migrations:
	docker exec -ti tas_development python3 manage.py makemigrations

log-django:
	docker-compose logs tas_developmentb

log-postgres:
	docker-compose logs tas_postgres_dbb
