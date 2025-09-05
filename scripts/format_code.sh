#!/bin/bash
# Code formatting script for Simple Grapher

set -e

echo "🎨 Formatting Simple Grapher code..."

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: Not in a virtual environment"
fi

# Format with black
echo "📝 Running Black formatter..."
python3 -m black simple_grapher/ tests/ examples/

# Sort imports with isort
echo "📦 Sorting imports with isort..."
python3 -m isort simple_grapher/ tests/ examples/

# Run linting
echo "🔍 Running linters..."
python3 -m flake8 simple_grapher/ tests/ || true
python3 -m mypy simple_grapher/ || true

echo "✅ Code formatting complete!"
echo ""
echo "💡 To set up formatting on save:"
echo "   1. Install VS Code extensions: Python, Black Formatter, isort"
echo "   2. Or run: make format"
echo "   3. Or use pre-commit hooks: git commit"
