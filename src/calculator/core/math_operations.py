"""Core mathematical operations for the Digital Special Calculator."""

from calculator.exceptions import DivisionByZeroError


def add(a: int | float, b: int | float) -> int | float:
    """Add two numbers together.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        The sum of a and b.
    """
    return a + b


def multiply(a: int | float, b: int | float) -> int | float:
    """Multiply two numbers together.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        The product of a and b.
    """
    return a * b


def divide(a: int | float, b: int | float) -> float:
    """Divide a by b.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        The quotient of a divided by b as a float.

    Raises:
        DivisionByZeroError: If b is zero.
    """
    if b == 0:
        raise DivisionByZeroError()
    return a / b
