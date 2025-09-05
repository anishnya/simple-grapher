# Simple Grapher

A command line tool for creating graphs. I find it to be quite useful.

## Quick Start

### Global installation
```bash
# Install globally (requires sudo)
./install.sh

# Then use from anywhere
simple-grapher --help
```

## Development

### Install in development mode
```bash
pip3 install -e . --user
pip3 install -r requirements-dev.txt --user
```

### Code Formatting & Linting

This project uses several tools to maintain code quality:

- **Black** - Code formatting
- **isort** - Import sorting
- **flake8** - Linting
- **mypy** - Type checking
- **pre-commit** - Git hooks

#### Formatting

**Manual Formatting:**
```bash
# Format all code
make format

# Check formatting without changing files
make format-check

# Run individual tools
python3 -m black simple_grapher/ tests/
python3 -m isort simple_grapher/ tests/
python3 -m flake8 simple_grapher/ tests/
python3 -m mypy simple_grapher/
```

**Pre-commit Hooks:**
```bash
# Install pre-commit hooks
python3 -m pre_commit install

# Run hooks on all files
python3 -m pre_commit run --all-files

# Hooks run automatically on git commit
git commit -m "Your commit message"
```

### Run tests
```bash
make test
# or
./scripts/run_tests.sh
```

### Project structure
```
simple-grapher/
├── simple_grapher/          # Main package
│   ├── cli.py              # Command line interface
│   ├── core/               # Core functionality
│   │   ├── config.py       # Configuration dataclasses
│   │   ├── data_processor.py # Data loading and processing
│   │   └── graph_builder.py # Graph creation and styling
│   └── utils/              # Utility functions
│       ├── helpers.py      # General helper functions
│       └── yaml_parser.py  # YAML configuration parsing
├── examples/               # Example configurations and generated graphs
│   ├── *.yaml             # Example YAML configuration files
│   ├── run_examples.py    # Script to generate example graphs
│   └── output/            # Generated graph images
├── tests/                  # Test suite
│   ├── test_cli.py        # CLI tests
│   ├── test_core.py       # Core functionality tests
│   ├── test_config.py     # Configuration tests
│   └── test_yaml_parser.py # YAML parser tests
├── scripts/                # Utility scripts
│   ├── format_code.sh     # Code formatting script
│   └── run_tests.sh       # Test runner script
├── pyproject.toml         # Project configuration
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── Makefile              # Build and development commands
├── install.sh            # Global installation script
└── simple-grapher        # Executable wrapper script
```

## Usage

```bash
# Show help
simple-grapher --help

# Show version
simple-grapher --version
```

## License

MIT License - see LICENSE file for details.
