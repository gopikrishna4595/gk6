.PHONY: install dev-install format lint type-check test check clean security quality lock release release-patch release-minor release-major security-check help

install:	## Install dependencies for end users
	poetry install

dev-install:	## Install everything needed for development (formatters, linters, hooks, etc.)
	poetry install
	poetry run pre-commit install

format:		## Format code with black and autofix lint issues with ruff
	poetry run ruff . --fix
	poetry run black .

lint:	## Lint without modifying code (e.g., in CI)
	poetry run ruff check .
	poetry run black --check .

type-check:		## Type check with mypy
	poetry run mypy .

test:	## Run all tests with coverage
	poetry run pytest -v --cov=gk6 --cov-report=term-missing

check:		## Run lint, type-check, and test
	make lint
	make type-check
	make test

clean:		## Clean generated files
	rm -rf .pytest_cache .mypy_cache .ruff_cache .venv dist build *.egg-info

security:		## Run bandit for security scanning
	poetry run bandit -r gk6

quality:		## Run format, lint, type-check, test, and security
	make format
	make check
	make security

lock: 	## Regenerate poetry.lock
	poetry lock

release-patch: ## Bump patch version, tag, and push
	poetry version patch
	git commit -am "🔖 Release v$$(poetry version -s)"
	git tag v$$(poetry version -s)
	git push && git push --tags

release-minor: ## Bump minor version, tag, and push
	poetry version minor
	git commit -am "🔖 Release v$$(poetry version -s)"
	git tag v$$(poetry version -s)
	git push && git push --tags

release-major: ## Bump major version, tag, and push
	poetry version major
	git commit -am "🔖 Release v$$(poetry version -s)"
	git tag v$$(poetry version -s)
	git push && git push --tags

release: release-patch ## Default release (patch bump)

publish-release:  ## Bump version, commit, tag, and push to trigger PyPI & GitHub Release
	poetry version patch
	git add pyproject.toml poetry.lock
	git commit -m "🔖 Release v$$(poetry version -s)"
	git tag v$$(poetry version -s)
	git push
	git push --tags

security-check:		## Tells Bandit to scan the entire directory recursively
	poetry run bandit -r gk6

help: ## Show available make commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
