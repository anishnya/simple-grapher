#!/bin/bash
# Test runner script for Simple Grapher

set -e

echo "Running Simple Grapher tests..."

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Warning: Not in a virtual environment"
fi

# Run tests
echo "Running unit tests..."
python -m pytest tests/ -v

# Run linting
echo "Running linting..."
python -m flake8 simple_grapher/ tests/

# Run type checking
echo "Running type checking..."
python -m mypy simple_grapher/

echo "All tests passed!"
