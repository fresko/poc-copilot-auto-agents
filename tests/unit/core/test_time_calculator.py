"""Tests for time calculator."""

from datetime import datetime, timedelta

from valet_parking.core.time_calculator import TimeCalculator


class TestTimeCalculator:
    """Tests for TimeCalculator class."""

    def test_calculate_duration_with_checkout_returns_difference(self, time_calculator):
        """Test that duration calculation with checkout time returns correct difference."""
        check_in = datetime(2024, 1, 15, 10, 0)
        check_out = datetime(2024, 1, 15, 12, 30)

        duration = time_calculator.calculate_duration(check_in, check_out)

        expected = timedelta(hours=2, minutes=30)
        assert duration == expected

    def test_calculate_duration_without_checkout_uses_current_time(self, time_calculator):
        """Test that duration calculation without checkout uses current time."""
        check_in = datetime.now() - timedelta(hours=1)

        duration = time_calculator.calculate_duration(check_in, None)

        # Should be approximately 1 hour (within 1 second tolerance)
        expected = timedelta(hours=1)
        assert abs(duration - expected) < timedelta(seconds=2)

    def test_calculate_duration_handles_same_time(self, time_calculator):
        """Test that same check-in and check-out time results in zero duration."""
        check_in = datetime(2024, 1, 15, 10, 0)
        check_out = datetime(2024, 1, 15, 10, 0)

        duration = time_calculator.calculate_duration(check_in, check_out)

        assert duration == timedelta(0)

    def test_calculate_parking_fee_correct_calculation(self, time_calculator):
        """Test that parking fee is calculated correctly."""
        duration = timedelta(hours=2, minutes=30)
        rate = 5.0

        fee = time_calculator.calculate_parking_fee(duration, rate)

        # 2.5 hours rounds up to 3 hours * $5 = $15
        assert fee == 15.0

    def test_calculate_parking_fee_rounds_up_partial_hours(self, time_calculator):
        """Test that partial hours are rounded up."""
        # Test with 2 hours and 1 minute
        duration = timedelta(hours=2, minutes=1)
        rate = 5.0

        fee = time_calculator.calculate_parking_fee(duration, rate)

        # Should round up to 3 hours
        assert fee == 15.0

    def test_calculate_parking_fee_exact_hours(self, time_calculator):
        """Test parking fee with exact hours."""
        duration = timedelta(hours=3)
        rate = 5.0

        fee = time_calculator.calculate_parking_fee(duration, rate)

        assert fee == 15.0

    def test_calculate_parking_fee_zero_duration(self, time_calculator):
        """Test parking fee with zero duration."""
        duration = timedelta(0)
        rate = 5.0

        fee = time_calculator.calculate_parking_fee(duration, rate)

        assert fee == 0.0
