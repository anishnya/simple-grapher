# Simple Grapher Makefile

.PHONY: help install install-dev test lint format clean build

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -r requirements-dev.txt
	pip install -e .

test:  ## Run tests
	python3 -m pytest tests/ -v

test-cov:  ## Run tests with coverage
	python3 -m pytest tests/ -v --cov=simple_grapher --cov-report=html

lint:  ## Run linting
	python3 -m flake8 simple_grapher/ tests/
	python3 -m mypy simple_grapher/

format:  ## Format code
	python3 -m black simple_grapher/ tests/
	python3 -m isort simple_grapher/ tests/

format-check:  ## Check code formatting
	python3 -m black --check simple_grapher/ tests/
	python3 -m isort --check-only simple_grapher/ tests/

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:  ## Build the package
	python setup.py sdist bdist_wheel

check: lint test  ## Run all checks (lint + test)
