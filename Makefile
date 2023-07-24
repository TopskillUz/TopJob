#!/usr/bin/make

include deploy/.env.dev

define SERVERS_JSON
{
	"Servers": {
		"1": {
			"Name": "topskill",
			"Group": "Servers",
			"Host": "$(DATABASE_HOST)",
			"Port": 5432,
			"MaintenanceDB": "postgres",
			"Username": "$(DATABASE_PASSWORD)",
			"SSLMode": "prefer",
			"PassFile": "/tmp/pgpassfile"
		}
	}
}
endef
export SERVERS_JSON
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
	docker compose -f docker-compose-prod.yml --env-file=.env.prod build
docker-down:
	rm -rf last.backup && docker exec -i topskill_db /bin/bash -c "PGPASSWORD=$(DATABASE_PASSWORD) pg_dump -Fc -h $(DATABASE_HOST) -U $(DATABASE_USER) $(DATABASE_NAME)" > $(PWD)/last.backup && docker compose -f docker-compose-prod.yml --env-file=.env.prod down && docker rmi python:3.10.6-slim
docker-up:
	docker compose -f docker-compose-prod.yml --env-file=.env.prod up -d --build && docker pull python:3.10.6-slim
monitoring-up:
	docker compose -f monitoring.yml --env-file=.env.prod up -d --build
monitoring-down:
	docker compose -f monitoring.yml --env-file=.env.prod down
pgadmin:
	docker compose -f pgadmin.yml --env-file=.env.prod up -d --build
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
initial-data:
	python code/app/initial_data.py
createsuperuser:
	python code/app/commands.py createsuperuser
createuser:
	python code/app/commands.py createuser
test:
	pytest -s -v -c code/pytest.ini