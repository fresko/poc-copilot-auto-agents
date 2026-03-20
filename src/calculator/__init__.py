"""Digital Special Calculator package.

Provides a calculator supporting sum, product, and division operations
with proper error handling for edge cases like division by zero.
"""

from calculator.core.calculator import SpecialCalculator
from calculator.exceptions import CalculatorError, DivisionByZeroError

__all__ = ["CalculatorError", "DivisionByZeroError", "SpecialCalculator"]
