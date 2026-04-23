.PHONY: install lint test seed migrate dev build

install:
	uv sync

lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy app

test:
	uv run pytest --cov=app --cov-fail-under=85

seed:
	uv run python -m app.seed

migrate:
	uv run alembic upgrade head

dev:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

build: lint test
