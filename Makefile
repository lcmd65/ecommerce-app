SHELL:=/bin/bash
include .env

# Docker compose commands
build:
	docker compose build
up:
	docker compose --env-file .env up
down:
	docker compose --env-file .env down
restart:
	make down && make up

# Start app in dev mode
run:
	@streamlit run app/fc.py --server.address 0.0.0.0 --server.port 8501 --browser.gatherUsageStats False & gunicorn -c config.py wsgi:app

flask:
	gunicorn -c config.py wsgi:app
