"""Tests for formatting utilities."""

from datetime import datetime, timedelta

from valet_parking.utils.formatters import format_parking_duration, format_timestamp


class TestFormatParkingDuration:
    """Tests for parking duration formatting."""

    def test_format_parking_duration_hours_and_minutes(self):
        """Test formatting duration with hours and minutes."""
        duration = timedelta(hours=2, minutes=30)
        result = format_parking_duration(duration)
        assert result == "2 hours 30 minutes"

    def test_format_parking_duration_days_hours_minutes(self):
        """Test formatting duration with days, hours, and minutes."""
        duration = timedelta(days=1, hours=3, minutes=15)
        result = format_parking_duration(duration)
        assert result == "1 day 3 hours 15 minutes"

    def test_format_parking_duration_only_minutes(self):
        """Test formatting duration with only minutes."""
        duration = timedelta(minutes=45)
        result = format_parking_duration(duration)
        assert result == "45 minutes"

    def test_format_parking_duration_zero(self):
        """Test formatting zero duration."""
        duration = timedelta(seconds=0)
        result = format_parking_duration(duration)
        assert result == "0 minutes"

    def test_format_parking_duration_negative(self):
        """Test formatting negative duration."""
        duration = timedelta(hours=-1)
        result = format_parking_duration(duration)
        assert result == "0 minutes"

    def test_format_parking_duration_singular_units(self):
        """Test that singular units are used correctly."""
        duration = timedelta(days=1, hours=1, minutes=1)
        result = format_parking_duration(duration)
        assert result == "1 day 1 hour 1 minute"


class TestFormatTimestamp:
    """Tests for timestamp formatting."""

    def test_format_timestamp_iso_format(self):
        """Test that timestamp is formatted in ISO format."""
        dt = datetime(2024, 1, 15, 14, 30, 0)
        result = format_timestamp(dt)
        assert result == "2024-01-15T14:30:00"

    def test_format_timestamp_with_microseconds(self):
        """Test formatting timestamp with microseconds."""
        dt = datetime(2024, 1, 15, 14, 30, 0, 123456)
        result = format_timestamp(dt)
        assert "2024-01-15T14:30:00" in result
