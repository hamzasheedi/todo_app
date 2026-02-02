"""
Utility functions for validation in the Todo CLI application.

This module provides various validation functions for input data, including date/time validation.
"""
from datetime import datetime
from typing import Union


def validate_iso_datetime(datetime_str: str) -> bool:
    """
    Validate that a string is in ISO 8601 format (date-only or datetime).
    Accepts both 'YYYY-MM-DD' and 'YYYY-MM-DDTHH:MM:SS' formats.

    Args:
        datetime_str: String to validate as ISO 8601 format

    Returns:
        True if the string is in valid ISO 8601 format, False otherwise
    """
    try:
        # Check if it's a date-only format (YYYY-MM-DD)
        if (len(datetime_str) == 10 and
            datetime_str.count('-') == 2 and
            '+' not in datetime_str and
            ':' not in datetime_str and
            'T' not in datetime_str and
            ' ' not in datetime_str and
            not datetime_str.endswith('Z')):
            # Try to parse as date
            date_parts = datetime_str.split('-')
            if len(date_parts) == 3:
                year, month, day = map(int, date_parts)
                # Validate date components
                datetime(year, month, day)
                return True

        # If it contains a space separator instead of 'T', it's not strictly ISO datetime
        if ' ' in datetime_str and 'T' not in datetime_str:
            return False  # Space separator is not allowed for strict ISO datetime

        # For datetime format, try to parse it
        parsed = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False


def parse_datetime(datetime_str: str) -> Union[datetime, None]:
    """
    Parse a datetime string in ISO 8601 format.

    Args:
        datetime_str: String in ISO 8601 format

    Returns:
        Parsed datetime object, or None if parsing fails
    """
    try:
        return datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
    except ValueError:
        return None


def validate_datetime_in_range(datetime_str: str, min_date: datetime = None, max_date: datetime = None) -> bool:
    """
    Validate that a datetime string falls within a specified range.

    Args:
        datetime_str: String in ISO 8601 format
        min_date: Minimum allowed date (optional)
        max_date: Maximum allowed date (optional)

    Returns:
        True if the datetime is in range, False otherwise
    """
    parsed_dt = parse_datetime(datetime_str)
    if parsed_dt is None:
        return False

    if min_date and parsed_dt < min_date:
        return False

    if max_date and parsed_dt > max_date:
        return False

    return True


def validate_timezone_format(datetime_str: str) -> bool:
    """
    Validate timezone format in datetime string.

    Args:
        datetime_str: String in ISO 8601 format

    Returns:
        True if the timezone format is valid, False otherwise
    """
    try:
        dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False


def normalize_datetime_string(datetime_str: str) -> str:
    """
    Normalize a datetime string to a consistent ISO 8601 format.

    Args:
        datetime_str: String in ISO 8601 format

    Returns:
        Normalized datetime string in ISO 8601 format

    Raises:
        ValueError: If the datetime string is not in a valid format
    """
    try:
        dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        return dt.isoformat()
    except ValueError:
        raise ValueError(f"Invalid datetime format: {datetime_str}")


def validate_future_datetime(datetime_str: str) -> bool:
    """
    Validate that a datetime string represents a future time.

    Args:
        datetime_str: String in ISO 8601 format

    Returns:
        True if the datetime is in the future, False otherwise
    """
    parsed_dt = parse_datetime(datetime_str)
    if parsed_dt is None:
        return False

    return parsed_dt > datetime.now()


def validate_datetime_with_grace_period(datetime_str: str, grace_minutes: int = 5) -> bool:
    """
    Validate that a datetime string is in the future, allowing for a grace period.

    This is useful for handling clock synchronization issues between client and server.

    Args:
        datetime_str: String in ISO 8601 format
        grace_minutes: Number of minutes before current time that's still acceptable (default: 5)

    Returns:
        True if the datetime is in the future (with grace period), False otherwise
    """
    parsed_dt = parse_datetime(datetime_str)
    if parsed_dt is None:
        return False

    # Allow for grace period
    from datetime import timedelta
    min_allowed = datetime.now().replace(second=0, microsecond=0) - timedelta(minutes=grace_minutes)
    return parsed_dt > min_allowed


def validate_concurrent_reminders(reminders: list, datetime_str: str, max_concurrent: int = 5) -> bool:
    """
    Validate that adding a new reminder won't exceed the maximum concurrent reminders.

    Args:
        reminders: List of existing reminders to check against
        datetime_str: Datetime for the new reminder
        max_concurrent: Maximum allowed concurrent reminders (default: 5)

    Returns:
        True if adding the reminder won't exceed the limit, False otherwise
    """
    if not reminders:
        return True

    new_dt = parse_datetime(datetime_str)
    if new_dt is None:
        return False

    # Count reminders that have the same time as the new reminder
    overlapping_count = 0
    for reminder in reminders:
        if hasattr(reminder, 'reminder_time'):
            existing_dt = parse_datetime(reminder.reminder_time)
            if existing_dt and existing_dt == new_dt:
                overlapping_count += 1

    # Check if the current number of concurrent reminders is within the limit
    # The count is the number of existing concurrent reminders
    # If overlapping_count equals max_concurrent, that means we're at the limit
    # which should be acceptable (not exceeded yet)
    return overlapping_count <= max_concurrent