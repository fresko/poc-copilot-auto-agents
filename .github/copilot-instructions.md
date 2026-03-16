# Python Project Guidelines

## Code Style

- **Python version**: 3.14.3+ (use modern syntax)
- **Formatting**: Use `ruff` for linting and formatting (replaces black, isort, flake8)
- **Type hints**: Always include type hints for function signatures and class attributes
- **Docstrings**: Use Google-style docstrings for modules, classes, and public functions
- **Import order**: Standard library → third-party → local (ruff handles automatically)
- **Line length**: 100 characters (balance readability with screen space)

## Project Structure

```
├── src/                    # Source code (installable package)
│   └── {package_name}/
│       ├── __init__.py
│       ├── core/          # Core business logic
│       ├── utils/         # Utility functions
│       └── models/        # Data models
├── tests/                 # Test files mirror src/ structure
│   ├── unit/
│   ├── integration/
│   └── conftest.py        # Shared pytest fixtures
├── scripts/               # Development and deployment scripts
├── docs/                  # Documentation
├── plan/                  # Planning documents
│   ├── in_doc/            # Planning documents for incoming requests    
│   └── out_doc/           # Planning documents for outgoing responses
├── pyproject.toml         # Project metadata and dependencies
├── README.md
└── .env.example          # Example environment variables
```

## Build and Test Commands

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
pytest -k "test_name"           # Specific test

# Run all checks (CI simulation)
ruff check . && mypy src/ && pytest
```

**Pre-commit:** Always run `ruff check --fix . && ruff format .` before committing.

## Testing Conventions

- **Test file naming**: `test_*.py` or `*_test.py`
- **Test function naming**: `test_<what>_<condition>_<expected>` (e.g., `test_user_login_invalid_credentials_returns_401`)
- **Fixtures**: Place shared fixtures in `tests/conftest.py`
- **Mocking**: Use `unittest.mock` or `pytest-mock` for dependencies
- **Assertions**: Prefer `assert` with clear messages over unittest-style assertions
- **Coverage target**: Aim for 80%+ coverage on core business logic

## Architecture Patterns

- **Dependency injection**: Pass dependencies as constructor parameters, not globals
- **Configuration**: Use Pydantic BaseSettings for environment variables
- **Error handling**: Create custom exception classes in `{package}/exceptions.py`
- **Logging**: Use standard library `logging`, configure at application entry point
- **Async code**: Use `asyncio` and `async/await`; prefix async functions with `async_` if mixing sync/async

## Type Hints Best Practices

```python
from typing import TypeAlias, Protocol, Literal
from collections.abc import Sequence, Mapping, Callable

# Use modern union syntax
def process(data: str | int | None) -> dict[str, Any]: ...

# Use Protocol for structural subtyping
class Closeable(Protocol):
    def close(self) -> None: ...

# Use TypeAlias for complex types
UserId: TypeAlias = int
UserMap: TypeAlias = dict[UserId, User]

# Use Literal for constrained values
Status: TypeAlias = Literal["pending", "active", "disabled"]
```

## Common Patterns

**Configuration management:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    debug_mode: bool = False
    
    class Config:
        env_file = ".env"
```

**Error handling:**
```python
class AppError(Exception):
    """Base exception for application-specific errors."""
    pass

class ValidationError(AppError):
    """Data validation failed."""
    pass
```

**Dependency injection example:**
```python
# Good: Dependencies injected
class UserService:
    def __init__(self, db: Database, cache: Cache):
        self.db = db
        self.cache = cache

# Avoid: Global state
# _db = Database()  # Global instance
```

## Dependencies Management

**pyproject.toml structure:**
```toml
[project]
name = "package-name"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "pydantic>=2.0",
    # Runtime dependencies
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.1",
    "pytest-asyncio>=0.23",
    "mypy>=1.8",
    "ruff>=0.3",
    # Development dependencies
]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "A", "C4", "PT"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
addopts = "-ra -q --strict-markers"
```

## When Creating New Files

- **Python files**: Always include module-level docstring and `if __name__ == "__main__":` guard for scripts
- **Test files**: Import from `src.package_name`, not relative imports
- **Init files**: Use `__all__` to explicitly declare public API
- **Config files**: Add comments explaining non-obvious settings

## Avoid

- ❌ Global mutable state
- ❌ `import *` (except in `__init__.py` with `__all__` defined)
- ❌ Bare `except:` clauses (always specify exception types)
- ❌ String formatting with `%` or `.format()` (use f-strings)
- ❌ Manual file handling (use context managers: `with open()`)
- ❌ Type ignores without explanation (`# type: ignore[specific-error]  # reason`)

## Agent Workflow Tips

1. **Before making changes**: Run `pytest` to establish baseline
2. **After code changes**: Run `ruff check --fix . && pytest` to verify
3. **For new features**: Create tests first (TDD), then implement
4. **For debugging**: Add `--pdb` flag to pytest for interactive debugging
5. **For dependencies**: Add to `pyproject.toml`, then `pip install -e ".[dev]"`
