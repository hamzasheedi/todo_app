"""
Tests for the validators utility module.
"""
from datetime import datetime, timedelta
from src.utils.validators import (
    validate_iso_datetime,
    parse_datetime,
    validate_datetime_in_range,
    validate_timezone_format,
    normalize_datetime_string,
    validate_future_datetime,
    validate_datetime_with_grace_period,
    validate_concurrent_reminders
)
from src.core.reminder import Reminder


def test_validate_iso_datetime():
    """Test ISO datetime validation."""
    # Valid formats
    valid_times = [
        "2025-12-31T10:00:00",
        "2025-12-31T10:00:00Z",
        "2025-12-31T10:00:00+00:00",
        "2025-12-31T10:00:00.123456",
        "2025-12-31T10:00:00.123456Z"
    ]

    for time_str in valid_times:
        assert validate_iso_datetime(time_str) is True

    # Invalid formats
    invalid_times = [
        "invalid-date",
        "2025-13-31T10:00:00",  # Invalid month
        "2025-12-32T10:00:00",  # Invalid day
        "2025-12-31",  # Just date, no time
        "2025-12-31 10:00:00",  # Wrong separator
        ""  # Empty string
    ]

    for time_str in invalid_times:
        assert validate_iso_datetime(time_str) is False


def test_parse_datetime():
    """Test datetime parsing."""
    valid_time = "2025-12-31T10:00:00"
    parsed = parse_datetime(valid_time)
    assert parsed is not None
    assert parsed.year == 2025
    assert parsed.month == 12
    assert parsed.day == 31

    invalid_time = "invalid-date"
    parsed = parse_datetime(invalid_time)
    assert parsed is None


def test_validate_datetime_in_range():
    """Test datetime range validation."""
    # Create range: 2025-01-01 to 2025-12-31
    min_date = datetime(2025, 1, 1)
    max_date = datetime(2025, 12, 31)

    # Valid within range
    assert validate_datetime_in_range("2025-06-15T10:00:00", min_date, max_date) is True

    # Outside range
    assert validate_datetime_in_range("2024-06-15T10:00:00", min_date, max_date) is False
    assert validate_datetime_in_range("2026-06-15T10:00:00", min_date, max_date) is False

    # Without bounds
    assert validate_datetime_in_range("2024-06-15T10:00:00") is True


def test_validate_timezone_format():
    """Test timezone format validation."""
    valid_tz = [
        "2025-12-31T10:00:00Z",
        "2025-12-31T10:00:00+00:00",
        "2025-12-31T10:00:00-05:00",
        "2025-12-31T10:00:00+05:30"
    ]

    for time_str in valid_tz:
        assert validate_timezone_format(time_str) is True

    # Test without timezone
    assert validate_timezone_format("2025-12-31T10:00:00") is True


def test_normalize_datetime_string():
    """Test datetime normalization."""
    input_time = "2025-12-31T10:00:00"
    normalized = normalize_datetime_string(input_time)
    assert normalized == "2025-12-31T10:00:00"

    input_time_with_tz = "2025-12-31T10:00:00Z"
    normalized = normalize_datetime_string(input_time_with_tz)
    assert "2025-12-31T10:00:00" in normalized

    # Test invalid input
    try:
        normalize_datetime_string("invalid")
        assert False, "Expected ValueError for invalid datetime"
    except ValueError:
        pass  # Expected


def test_validate_future_datetime():
    """Test future datetime validation."""
    future_time = (datetime.now() + timedelta(hours=1)).isoformat()
    assert validate_future_datetime(future_time) is True

    past_time = (datetime.now() - timedelta(hours=1)).isoformat()
    assert validate_future_datetime(past_time) is False

    invalid_time = "invalid"
    assert validate_future_datetime(invalid_time) is False


def test_validate_datetime_with_grace_period():
    """Test datetime validation with grace period."""
    # Future time should be valid
    future_time = (datetime.now() + timedelta(hours=1)).isoformat()
    assert validate_datetime_with_grace_period(future_time) is True

    # Past time within grace period should be valid
    past_time = (datetime.now() - timedelta(minutes=1)).isoformat()
    assert validate_datetime_with_grace_period(past_time, grace_minutes=5) is True

    # Past time outside grace period should be invalid
    past_time = (datetime.now() - timedelta(minutes=10)).isoformat()
    assert validate_datetime_with_grace_period(past_time, grace_minutes=5) is False


def test_validate_concurrent_reminders():
    """Test concurrent reminders validation."""
    # Create some test reminders
    future_time = (datetime.now() + timedelta(hours=1)).isoformat()

    reminder1 = Reminder(task_id="task1", reminder_time=future_time)
    reminder2 = Reminder(task_id="task2", reminder_time=future_time)  # Same time
    reminder3 = Reminder(task_id="task3", reminder_time=future_time)  # Same time

    reminders = [reminder1, reminder2, reminder3]

    # Should allow up to max_concurrent (default 5)
    assert validate_concurrent_reminders(reminders, future_time) is True

    # Create more reminders to exceed limit
    reminder4 = Reminder(task_id="task4", reminder_time=future_time)
    reminder5 = Reminder(task_id="task5", reminder_time=future_time)
    reminder6 = Reminder(task_id="task6", reminder_time=future_time)  # This makes 6 total

    reminders = [reminder1, reminder2, reminder3, reminder4, reminder5, reminder6]

    # Should reject because it exceeds default limit of 5
    assert validate_concurrent_reminders(reminders, future_time) is False

    # With custom limit of 6, it should pass
    assert validate_concurrent_reminders(reminders, future_time, max_concurrent=6) is True

    # With a different time, it should pass regardless
    different_time = (datetime.now() + timedelta(hours=2)).isoformat()
    assert validate_concurrent_reminders(reminders, different_time) is True