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
	docker compose up -d postgresql

run:
	make upgrade || make upgrade || true
	python -m uvicorn service.__main__:app  --host 0.0.0.0 --port=${FASTAPI_PORT} --log-level=warning --reload &

run-worker:
	make migrate
	python -m worker

migrate:
	cd migrations && python -m alembic upgrade head

upgrade:
	cd migrations && python -m alembic upgrade +1

downgrade:
	cd migrations && python -m alembic downgrade -1

revision:
	cd migrations && python -m alembic revision --autogenerate
