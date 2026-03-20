"""Custom exceptions for the Digital Special Calculator module."""


class CalculatorError(Exception):
    """Base exception for all calculator errors."""


class DivisionByZeroError(CalculatorError):
    """Raised when division by zero is attempted."""

    def __init__(self) -> None:
        super().__init__("Division by zero is not allowed.")
