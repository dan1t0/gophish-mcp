# Test Organization Structure

## 📁 Directory Structure

```
tests/
├── __init__.py
├── README.md
├── ORGANIZATION.md
├── run_tests.py              # Main test runner script
├── demo_verbose.py           # Verbose demo script
├── run_comprehensive_tests.py # Comprehensive test runner
├── scripts/                  # Main test scripts
│   ├── test_readonly_tools.py # Read-only tools test suite
│   └── demo_verbose.py       # Verbose demo (duplicate)
├── comprehensive/            # Comprehensive tests
│   └── test_comprehensive.py # Comprehensive test suite
└── individual/               # Individual test modules
    ├── __init__.py
    ├── test_connection.py    # Basic connection tests
    ├── test_advanced_features.py  # Advanced MCP features tests
    └── test_diagnosis.py     # Connectivity diagnosis tests
```

## 🚀 How to Run Tests

### Run All Tests (Recommended)
```bash
# From project root
python test.py all
```

### Run Specific Test Types
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

### Run Individual Tests
```bash
# Run all individual tests
pytest tests/individual/ -v

# Run specific individual test
pytest tests/individual/test_connection.py -v

# Run comprehensive test
python test.py comprehensive
```

### Run from Tests Directory
```bash
cd tests
python run_tests.py
python demo_verbose.py
python run_comprehensive_tests.py
```

## 📋 Test Types

### Individual Tests (`individual/`)
- **Purpose**: Focused, unit-style tests for specific functionality
- **Framework**: pytest
- **Execution**: `pytest tests/individual/ -v`
- **Files**:
  - `test_connection.py`: Basic GoPhish connection tests
  - `test_advanced_features.py`: Advanced MCP features tests
  - `test_diagnosis.py`: Connectivity and diagnosis tests

### Main Test Scripts (`scripts/`)
- **Purpose**: Main test suites and utilities
- **Framework**: Standalone asyncio scripts
- **Execution**: `python test.py readonly` or `python test.py demo`
- **Files**:
  - `test_readonly_tools.py`: Complete read-only tools test suite
  - `demo_verbose.py`: Verbose demo with colored output

### Comprehensive Test (`comprehensive/`)
- **Purpose**: End-to-end test of all MCP functionality
- **Framework**: Standalone asyncio script
- **Execution**: `python test.py comprehensive`
- **Features**: Tests all 42+ MCP tools in sequence

## 🔧 Benefits of This Organization

1. **Clear Separation**: Individual tests vs main scripts vs comprehensive test
2. **No Confusion**: Clear distinction between what to run and how
3. **Flexibility**: Can run individual tests, main scripts, or everything
4. **Maintainability**: Easy to add new individual tests or main scripts
5. **CI/CD Ready**: Both pytest and standalone execution supported
6. **User Friendly**: Simple `python test.py` commands from project root

## 📝 Adding New Tests

### Individual Test
1. Create new file in `individual/` folder
2. Use pytest framework
3. Follow naming convention: `test_*.py`
4. Run with: `pytest tests/individual/your_test.py -v`

### Main Test Script
1. Create new file in `scripts/` folder
2. Use asyncio framework
3. Add command to `test.py` main script
4. Run with: `python test.py your_command`

### Comprehensive Test Addition
1. Add new test function to `comprehensive/test_comprehensive.py`
2. Call it from the main execution block
3. Run with: `python test.py comprehensive`

## 🎯 Usage Examples

```bash
# Quick individual test
pytest tests/individual/test_connection.py -v

# All individual tests
pytest tests/individual/ -v

# Main test suites
python test.py readonly
python test.py demo

# Full comprehensive test
python test.py comprehensive

# Everything (recommended)
python test.py all

# From tests directory
cd tests
python run_tests.py
python demo_verbose.py
```