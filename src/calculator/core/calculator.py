"""SpecialCalculator class providing the primary interface for calculator operations."""

from calculator.core.math_operations import add, divide, multiply


class SpecialCalculator:
    """A digital special calculator supporting sum, product, and div operations.

    This class wraps the core mathematical operations and exposes them as a
    clean business logic interface.

    Example:
        >>> calc = SpecialCalculator()
        >>> calc.sum(2, 3)
        5
        >>> calc.product(4, 5)
        20
        >>> calc.div(10, 2)
        5.0
    """

    def sum(self, a: int | float, b: int | float) -> int | float:
        """Return the sum of two numbers.

        Args:
            a: The first operand.
            b: The second operand.

        Returns:
            The sum of a and b.
        """
        return add(a, b)

    def product(self, a: int | float, b: int | float) -> int | float:
        """Return the product of two numbers.

        Args:
            a: The first operand.
            b: The second operand.

        Returns:
            The product of a and b.
        """
        return multiply(a, b)

    def div(self, a: int | float, b: int | float) -> float:
        """Return the quotient of a divided by b.

        Args:
            a: The dividend.
            b: The divisor.

        Returns:
            The quotient of a divided by b as a float.

        Raises:
            DivisionByZeroError: If b is zero.
        """
        return divide(a, b)


__all__ = ["SpecialCalculator"]
