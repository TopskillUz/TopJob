#!/usr/bin/make
export PYTHONPATH=:$(PWD)/code/app

help:
	@echo "make"
	@echo "	hello"
	@echo "		print hello world"
	@echo "	init-locale"
	@echo "		Initialize locale messages: make update-locale ARGS='ru'"

hello:
	echo "Hello, World"
run:
	cd code && python main.py
docker-build:
	docker compose -f deploy/docker-compose-prod.yml --env-file=deploy/.env.prod build --progress=plain
docker-down:
	docker compose -f deploy/docker-compose-prod.yml --env-file=deploy/.env.prod down
docker-up:
	docker compose -f deploy/docker-compose-prod.yml --env-file=deploy/.env.prod up -d --build
alembic-head:
	cd code && alembic upgrade head
alembic-revision:
	cd code && alembic revision --autogenerate -m '$(ARGS)'
env:
	source venv/bin/activate
extract-locale:
	pybabel extract -F code/app/babel.cfg -o code/app/locales/messages.pot code/app
init-locale:
	pybabel init -i code/app/locales/messages.pot -d code/app/locales -l $(ARGS)
update-locale:
	pybabel update -i code/app/locales/messages.pot -d code/app/locales -l $(ARGS)
compile-locale:
	pybabel compile -d code/app/locales