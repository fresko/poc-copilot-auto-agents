# Digital Special Calculator Implementation Plan

## Overview
Create a "Digital Special" calculator module in Python that supports three core operations: `sum` (addition), `product` (multiplication), and `div` (division). This calculator will form the core logic within the established project architecture.

## Requirements
1. **Core Operations**: Support `sum`, `product`, and `div` for numeric inputs (integers and floats).
2. **Error Handling**: Properly handle edge cases, specifically division by zero.
3. **Type Safety**: Use robust Python 3 type hints for all parameters and return types.
4. **Code Quality**: Adhere to `ruff` formatting, Google-style docstrings, and strict `mypy` typing.
5. **Testing**: Accompanied by unit tests providing high coverage (minimally 80%+) following the defined `pytest` project conventions.

## Implementation Steps

1. **Implement Custom Exceptions**
   - **File**: `src/calculator/exceptions.py`
   - **Action**: Create a base `CalculatorError` exception and a specific `DivisionByZeroError` exception to handle division failures cleanly.

2. **Implement Core Mathematical Logic**
   - **File**: `src/calculator/core/math_operations.py`
   - **Action**: Implement typed standalone functions:
     - `add(a: int | float, b: int | float) -> int | float`
     - `multiply(a: int | float, b: int | float) -> int | float`
     - `divide(a: int | float, b: int | float) -> float` (Raises `DivisionByZeroError` if `b == 0`)

3. **Implement Calculator Interface**
   - **File**: `src/calculator/core/calculator.py`
   - **Action**: Create a `SpecialCalculator` class that wraps the underlying math operations, exposing `sum`, `product`, and `div` methods to external callers as the primary business logic interface.

4. **Module Initialization**
   - **File**: `src/calculator/__init__.py` and `src/calculator/core/__init__.py`
   - **Action**: Define `__all__` to expose the `SpecialCalculator` and custom exceptions gracefully to users of the package.

## Testing Plan
All tests will be placed in the `tests/unit/` directory. 

**Test Cases to Implement:**
1. **Sum Operations**
   - `test_sum_positive_numbers_returns_correct_sum`
   - `test_sum_negative_numbers_returns_correct_sum`
   - `test_sum_with_floats_returns_accurate_float`
2. **Product Operations**
   - `test_product_positive_numbers_returns_correct_product`
   - `test_product_with_zero_returns_zero`
   - `test_product_with_floats_returns_accurate_float`
3. **Division Operations**
   - `test_div_valid_numbers_returns_correct_quotient`
   - `test_div_by_zero_raises_division_by_zero_error`
   - `test_div_with_floats_returns_accurate_float`

After implementing the tests and codebase, run:
```bash
ruff check --fix .
ruff format .
mypy src/
pytest tests/unit/
```