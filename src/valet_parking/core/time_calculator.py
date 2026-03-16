"""Time calculation utilities for parking duration and fees."""

from datetime import datetime, timedelta


class TimeCalculator:
    """Calculate parking duration and fees.

    Handles calculation of time elapsed and parking fees based on hourly rates.
    """

    def calculate_duration(
        self, check_in: datetime, check_out: datetime | None = None
    ) -> timedelta:
        """Calculate parking duration.

        Args:
            check_in: Time when vehicle was checked in.
            check_out: Time when vehicle was checked out. If None, uses current time.

        Returns:
            Time duration between check-in and check-out (or now).

        Examples:
            >>> calculator = TimeCalculator()
            >>> check_in = datetime(2024, 1, 15, 10, 0)
            >>> check_out = datetime(2024, 1, 15, 12, 30)
            >>> duration = calculator.calculate_duration(check_in, check_out)
            >>> duration.total_seconds() / 3600
            2.5
        """
        end_time = check_out if check_out is not None else datetime.now()
        return end_time - check_in

    def calculate_parking_fee(self, duration: timedelta, rate_per_hour: float) -> float:
        """Calculate parking fee based on duration and hourly rate.

        Rounds up partial hours to the next full hour.

        Args:
            duration: Parking duration.
            rate_per_hour: Hourly parking rate.

        Returns:
            Total parking fee rounded to 2 decimal places.

        Examples:
            >>> calculator = TimeCalculator()
            >>> duration = timedelta(hours=2, minutes=30)
            >>> calculator.calculate_parking_fee(duration, 5.0)
            15.0
            >>> duration = timedelta(hours=2, minutes=1)
            >>> calculator.calculate_parking_fee(duration, 5.0)
            15.0
        """
        hours = duration.total_seconds() / 3600

        # Round up partial hours
        import math

        billable_hours = math.ceil(hours)

        fee = billable_hours * rate_per_hour
        return round(fee, 2)
