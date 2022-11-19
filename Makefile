include .env
export

prepare:
	pip install -r requirements.txt

prepare-local:
	python3 -m venv .venv
	. .venv/bin/activate
	pip install -r requirements.txt

services:
	docker compose down
	docker compose up -d

run:
	uvicorn service.__main__:app  --host 0.0.0.0 --port=${FASTAPI_PORT} --log-level=warning --reload

migrate:
	cd migrations && alembic upgrade head

downgrade:
	cd migrations && alembic downgrade -1

revision:
	cd migrations && alembic revision --autogenerate