"""Unit tests for the Digital Special Calculator."""

import pytest

from calculator import DivisionByZeroError, SpecialCalculator


class TestSpecialCalculatorSum:
    """Tests for the SpecialCalculator.sum method."""

    def test_sum_positive_numbers_returns_correct_sum(self) -> None:
        calc = SpecialCalculator()
        assert calc.sum(3, 5) == 8

    def test_sum_negative_numbers_returns_correct_sum(self) -> None:
        calc = SpecialCalculator()
        assert calc.sum(-4, -6) == -10

    def test_sum_with_floats_returns_accurate_float(self) -> None:
        calc = SpecialCalculator()
        assert calc.sum(1.5, 2.5) == pytest.approx(4.0)


class TestSpecialCalculatorProduct:
    """Tests for the SpecialCalculator.product method."""

    def test_product_positive_numbers_returns_correct_product(self) -> None:
        calc = SpecialCalculator()
        assert calc.product(4, 5) == 20

    def test_product_with_zero_returns_zero(self) -> None:
        calc = SpecialCalculator()
        assert calc.product(99, 0) == 0

    def test_product_with_floats_returns_accurate_float(self) -> None:
        calc = SpecialCalculator()
        assert calc.product(2.5, 4.0) == pytest.approx(10.0)


class TestSpecialCalculatorDiv:
    """Tests for the SpecialCalculator.div method."""

    def test_div_valid_numbers_returns_correct_quotient(self) -> None:
        calc = SpecialCalculator()
        assert calc.div(10, 2) == pytest.approx(5.0)

    def test_div_by_zero_raises_division_by_zero_error(self) -> None:
        calc = SpecialCalculator()
        with pytest.raises(DivisionByZeroError):
            calc.div(5, 0)

    def test_div_with_floats_returns_accurate_float(self) -> None:
        calc = SpecialCalculator()
        assert calc.div(7.5, 2.5) == pytest.approx(3.0)
