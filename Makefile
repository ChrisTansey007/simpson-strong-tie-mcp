.PHONY: bootstrap lock format lint typecheck test test-integration migrate compose-up compose-down api mcp worker web verify

bootstrap:
	uv sync --all-packages --dev
	npm install

lock:
	uv lock

format:
	uv run ruff format .

lint:
	uv run ruff check .
	npm run lint

typecheck:
	uv run pyright
	npm run typecheck

test:
	uv run pytest
	npm test -- --run

test-integration:
	uv run pytest -m integration

migrate:
	uv run alembic upgrade head

compose-up:
	docker compose up -d

compose-down:
	docker compose down

api:
	uv run simpson-api

mcp:
	uv run simpson-mcp

worker:
	uv run simpson-worker

web:
	npm run dev

verify:
	uv run ruff format --check .
	uv run ruff check .
	uv run pyright
	uv run pytest
	npm run lint
	npm run typecheck
	npm test -- --run
	docker compose config
