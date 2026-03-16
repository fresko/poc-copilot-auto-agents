"""Formatting utilities for displaying data."""

from datetime import datetime, timedelta


def format_parking_duration(duration: timedelta) -> str:
    """Format parking duration in human-readable format.

    Args:
        duration: Time duration to format.

    Returns:
        Human-readable duration string (e.g., "2 hours 30 minutes").

    Examples:
        >>> format_parking_duration(timedelta(hours=2, minutes=30))
        '2 hours 30 minutes'
        >>> format_parking_duration(timedelta(days=1, hours=3))
        '1 day 3 hours'
    """
    total_seconds = int(duration.total_seconds())

    if total_seconds < 0:
        return "0 minutes"

    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60

    parts = []

    if days > 0:
        parts.append(f"{days} {'day' if days == 1 else 'days'}")

    if hours > 0:
        parts.append(f"{hours} {'hour' if hours == 1 else 'hours'}")

    if minutes > 0:
        parts.append(f"{minutes} {'minute' if minutes == 1 else 'minutes'}")

    if not parts:
        return "0 minutes"

    return " ".join(parts)


def format_timestamp(dt: datetime) -> str:
    """Format datetime in ISO format with timezone.

    Args:
        dt: Datetime to format.

    Returns:
        ISO formatted datetime string.

    Examples:
        >>> format_timestamp(datetime(2024, 1, 15, 14, 30))
        '2024-01-15T14:30:00'
    """
    return dt.isoformat()
