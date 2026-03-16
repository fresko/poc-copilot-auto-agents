# Project Guidelines

## Code Style

- **Python version**: 3.14.3+ (use modern syntax)
- **Formatting**: Use `ruff` for linting and formatting (replaces black, isort, flake8)
- **Type hints**: Always include type hints for function signatures and class attributes
- **Docstrings**: Use Google-style docstrings for modules, classes, and public functions
- **Import order**: Standard library → third-party → local (ruff handles automatically)
- **Line length**: 100 characters (balance readability with screen space)

## Architecture

**Project Structure**:
```
├── src/                    # Source code (installable package)
│   └── {package_name}/
│       ├── __init__.py
│       ├── core/          # Core business logic
│       ├── utils/         # Utility functions
│       └── models/        # Data models
├── tests/                 # Test files mirror src/ structure
├── scripts/               # Development and deployment scripts
├── docs/                  # Documentation
├── plan/                  # Planning documents
│   ├── in_doc/            # Planning documents for incoming requests    
│   └── out_doc/           # Planning documents for outgoing responses
├── pyproject.toml         # Project metadata and dependencies
└── README.md
```

**Architecture Patterns**:
- **Dependency injection**: Pass dependencies as constructor parameters, not globals
- **Configuration**: Use Pydantic BaseSettings for environment variables
- **Error handling**: Create custom exception classes in `{package}/exceptions.py`
- **Logging**: Use standard library `logging`, configure at application entry point
- **Async code**: Use `asyncio` and `async/await`; prefix async functions with `async_` if mixing sync/async

## Build and Test

**Setup environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"    # Install package in editable mode with dev dependencies
```

**Development workflow:**
```bash
# Format code
ruff check --fix .
ruff format .

# Type check
mypy src/

# Run tests
pytest                           # All tests
pytest tests/unit/              # Unit tests only
pytest -v --cov=src tests/      # With coverage report

# Run all checks (CI simulation)
ruff check . && mypy src/ && pytest
```

**Testing Conventions**:
- **File naming**: `test_*.py` or `*_test.py`
- **Function naming**: `test_<what>_<condition>_<expected>` (e.g., `test_user_login_invalid_credentials_returns_401`)
- **Fixtures**: Place shared fixtures in `tests/conftest.py`
- **Mocking**: Use `unittest.mock` or `pytest-mock` for dependencies
- **Coverage target**: Aim for 80%+ coverage on core business logic

## Conventions

**Type Hints**:
- Use modern union syntax (`str | int | None`)
- Use `Protocol` for structural subtyping
- Use `TypeAlias` for complex types and `Literal` for constrained values

**When Creating New Files**:
- **Python files**: Always include module-level docstring and `if __name__ == "__main__":` guard for scripts
- **Test files**: Import from `src.package_name`, not relative imports
- **Init files**: Use `__all__` to explicitly declare public API

**Agent Workflow Tips**:
1. **Before making changes**: Run `pytest` to establish baseline
2. **After code changes**: Run `ruff check --fix . && pytest` to verify
3. **For new features**: Create tests first (TDD), then implement
4. **Dependencies**: Add to `pyproject.toml`, then `pip install -e ".[dev]"`

