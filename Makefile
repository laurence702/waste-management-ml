.PHONY: up down restart logs build migrate test

up:
	docker compose up -d

down:
	docker compose down

restart: down up

logs:
	docker compose logs -f

build:
	docker compose up -d --build

migrate:
	docker compose exec backend alembic revision --autogenerate -m "auto"
	docker compose exec backend alembic upgrade head

test:
	docker compose exec backend python -m pytest

seed:
	docker compose exec backend python scripts/seed.py

sh:
	docker compose exec backend bash
