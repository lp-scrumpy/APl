-include .env
export

dev.install:
	@poetry install
lint:
	@mypy backend
	@flake8 backend
run: 
	@python -m backend

db.run:
	@docker-compose up -d db

db.create:
	@python -m backend.models

db.stop:
	@docker-compose stop db

stop: 
	@docker-compose stop -t 1

clean:
	@docker-compose down
