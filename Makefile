POETRY ?= $(HOME)/.poetry/bin/poetry

.PHONY: install-poetry
install-poetry:
	@curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

.PHONY: install-deps
install-deps:
	@$(POETRY) install -E aiohttp_backend -vv

.PHONY: fmt
fmt:
	@poetry run isort --recursive .
	@poetry run black .

.PHONY: clean
clean:
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete
	@rm -rf build dist .coverage MANIFEST

.PHONY: check-release
check-release:
	@pip install --upgrade twine
	@poetry build
	@twine check dist/*
	@rm -rf build dist .coverage MANIFEST

.PHONY: test
test:
	@poetry run py.test -vv --cov-report term-missing --cov=pornhub_api tests

.PHONY: lint-flake8
flake8:
	@poetry run flake8 pornhub_api tests

.PHONY: lint-isort
isort:
	@poetry run isort -rc --diff pornhub_apii

.PHONY: lint-mypy
lint-mypy:
	@poetry run mypy pornhub_api

.PHONY: lint-black
lint-black:
	@poetry run black --diff --check .

.PHONY: lint-bandit
lint-bandit:
	@poetry run bandit .

.PHONY: lint
lint: lint-isort lint-flake8 lint-black lint-mypy lint-bandit

.PHONY: check
check: lint test
