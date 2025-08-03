.PHONY: install dev-install format lint type-check test check clean security quality lock release security-check help

install: ## Install dependencies for end users
	poetry install

dev-install: ## Install everything needed for development (formatters, linters, hooks, etc.)
	poetry install
	poetry run pre-commit install

format: ## Format code with black and autofix lint issues with ruff and isort
	poetry run ruff format .
	poetry run ruff check . --fix
	poetry run isort . --profile black
	poetry run black .

lint: ## Lint without modifying code (e.g., in CI)
	poetry run ruff check .
	poetry run isort . --check --diff --profile black
	poetry run black --check .

type-check: ## Type check with mypy
	poetry run mypy .

test:	## Run all tests with coverage
	poetry run pytest -v --cov=gk6 --cov-report=term-missing

check: ## Run lint, type-check, and test
	make lint
	make type-check
	make test

clean: ## Clean generated files
	rm -rf .pytest_cache .mypy_cache .ruff_cache .venv dist build *.egg-info

security-check: ## Run bandit for security scanning
	poetry run bandit -r gk6

quality: ## Run format, lint, type-check, test, and security
	make format
	make check
	make security-check

lock: ## Regenerate poetry.lock
	poetry lock

release-patch: ## Bump patch version, tag, and push
	poetry version patch
	git add pyproject.toml poetry.lock
	git commit -m "🔖 Release v$$(poetry version -s)"
	git tag v$$(poetry version -s)
	git push && git push --tags

publish-release: ## Bump version, commit, push and trigger PyPI release
	make release

help: ## Show available make commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
