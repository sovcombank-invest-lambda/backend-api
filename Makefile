prepare:
	echo preapring

services:
	echo services

run:
	echo run

migrate:
	cd migrator && alembic upgrade head

downgrade:
	cd migrator && alembic downgrade -1

revision:
	cd migrator && alembic revision --autogenerate