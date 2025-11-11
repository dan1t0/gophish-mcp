# Tests for GoPhish MCP Server

This directory contains all tests for the GoPhish MCP server.

## Configuration

1. Copy `env.example` to `.env` in the project root directory
2. Configure your GoPhish credentials in the `.env` file:

```bash
GOPHISH_URL=https://your-gophish-server:3333
GOPHISH_API_KEY=your-api-key-here
```

## Running Tests

### Run all tests
```bash
python test.py all
```

### Run specific test types
```bash
# Read-only tests
python test.py readonly

# Verbose demo
python test.py demo

# Comprehensive tests
python test.py comprehensive

# With verbose output
python test.py readonly --verbose
```

### Run individual tests
```bash
# Basic connection test
python -m pytest tests/individual/test_connection.py -v

# Advanced features test
python -m pytest tests/individual/test_advanced_features.py -v

# Diagnosis test
python -m pytest tests/individual/test_diagnosis.py -v

# All individual tests
pytest tests/individual/ -v
```

### Run from tests directory
```bash
cd tests
python run_tests.py
python demo_verbose.py
python run_comprehensive_tests.py
```

## File Structure

### Individual Tests (`individual/`)
- `test_connection.py`: Basic GoPhish connection tests
- `test_advanced_features.py`: Advanced MCP features tests
- `test_diagnosis.py`: Connectivity diagnosis tests

### Main Test Scripts
- `test_comprehensive.py`: Comprehensive test of all functionalities
- `run_tests.py`: Main script to run all tests
- `demo_verbose.py`: Verbose demo script
- `run_comprehensive_tests.py`: Comprehensive test runner

### Organized Subdirectories
- `scripts/`: Main test scripts (test_readonly_tools.py, demo_verbose.py)
- `comprehensive/`: Comprehensive test suite
- `individual/`: Individual test modules

## Requirements

- Python 3.8+
- GoPhish server running
- Valid credentials configured in `.env`
- Dependencies installed: `pip install -e .`

## Notes

- Tests require a running GoPhish server
- Some tests may fail if there's no data in GoPhish
- Write tests (create/update/delete) are disabled by default
- Use `python test.py` from project root for easiest execution