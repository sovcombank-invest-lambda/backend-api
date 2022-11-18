prepare:
	echo preparing
	
services:
	echo bringin up services

run:
	echo running up

migrate:
	cd migrator && alembic upgrade head

downgrade:
	cd migrator && alembic downgrade -1

revision:
	cd migrator && alembic revision --autogenerate