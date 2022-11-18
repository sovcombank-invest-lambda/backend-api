include .env
export

prepare:
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt

services:
	docker compose up -d
	make migrate

run:
	uvicorn service.__main__:app  --host 0.0.0.0 --port=${FASTAPI_PORT} --log-level=warning --reload

migrate:
	cd migrator && alembic upgrade head

downgrade:
	cd migrator && alembic downgrade -1

revision:
	cd migrator && alembic revision --autogenerate