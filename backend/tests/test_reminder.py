"""
Tests for the Reminder entity class.
"""
from datetime import datetime, timedelta
from src.core.reminder import Reminder, ReminderStatus


def test_reminder_creation():
    """Test basic reminder creation."""
    future_time = (datetime.now() + timedelta(hours=1)).isoformat()

    # Create a reminder
    reminder = Reminder(
        task_id="task123",
        reminder_time=future_time
    )

    assert reminder.task_id == "task123"
    assert reminder.reminder_time == future_time
    assert reminder.is_triggered is False
    assert reminder.status == ReminderStatus.PENDING
    assert reminder.id is not None


def test_reminder_validation():
    """Test reminder validation rules."""
    future_time = (datetime.now() + timedelta(hours=1)).isoformat()
    past_time = (datetime.now() - timedelta(hours=1)).isoformat()

    # Test that reminder time must be in the future
    try:
        Reminder(
            task_id="task123",
            reminder_time=past_time
        )
        assert False, "Expected ValueError for past reminder time"
    except ValueError:
        pass  # Expected

    # Test task ID validation
    try:
        Reminder(
            task_id="",  # Empty task ID
            reminder_time=future_time
        )
        assert False, "Expected ValueError for empty task ID"
    except ValueError:
        pass  # Expected

    # Test invalid status
    try:
        reminder = Reminder(
            task_id="task123",
            reminder_time=future_time
        )
        reminder.status = "invalid_status"
        assert False, "Expected ValueError for invalid status"
    except ValueError:
        pass  # Expected


def test_is_overdue():
    """Test the is_overdue method."""
    future_time = (datetime.now() + timedelta(hours=1)).isoformat()

    # Create a reminder with future time
    reminder = Reminder(
        task_id="task123",
        reminder_time=future_time
    )

    assert reminder.is_overdue() is False

    # Now simulate that the time has passed by directly modifying the internal state
    past_time = (datetime.now() - timedelta(minutes=1)).isoformat()
    reminder._reminder_time = past_time  # Bypass validation for testing

    # With past time and not triggered, it should be overdue
    assert reminder.is_overdue() is True

    # Create another reminder with future time
    reminder2 = Reminder(
        task_id="task456",
        reminder_time=future_time
    )

    assert reminder2.is_overdue() is False

    # Create a reminder with past time but already triggered
    reminder3 = Reminder(
        task_id="task789",
        reminder_time=future_time
    )

    # Simulate past time and already triggered
    reminder3._reminder_time = past_time  # Bypass validation for testing
    reminder3.is_triggered = True

    assert reminder3.is_overdue() is False


def test_should_trigger():
    """Test the should_trigger method."""
    future_time = (datetime.now() + timedelta(hours=1)).isoformat()

    # Create a pending reminder with future time (should not trigger initially)
    reminder = Reminder(
        task_id="task123",
        reminder_time=future_time
    )

    assert reminder.should_trigger() is False

    # Now simulate that the time has passed by directly modifying the internal state
    past_time = (datetime.now() - timedelta(minutes=1)).isoformat()
    reminder._reminder_time = past_time  # Bypass validation for testing

    # With past time and not triggered, it should trigger
    assert reminder.should_trigger() is True

    # Create a pending reminder with future time (should not trigger)
    reminder2 = Reminder(
        task_id="task456",
        reminder_time=future_time
    )

    assert reminder2.should_trigger() is False

    # Create a triggered reminder with past time (should not trigger again)
    reminder3 = Reminder(
        task_id="task789",
        reminder_time=future_time
    )

    # Simulate past time and already triggered
    reminder3._reminder_time = past_time  # Bypass validation for testing
    reminder3.is_triggered = True

    assert reminder3.should_trigger() is False

    # Create a cancelled reminder (should not trigger)
    reminder4 = Reminder(
        task_id="taskabc",
        reminder_time=future_time
    )
    reminder4.cancel()

    # Simulate past time for cancelled reminder
    reminder4._reminder_time = past_time  # Bypass validation for testing

    assert reminder4.should_trigger() is False


def test_trigger_method():
    """Test the trigger method."""
    future_time = (datetime.now() + timedelta(hours=1)).isoformat()

    reminder = Reminder(
        task_id="task123",
        reminder_time=future_time
    )

    # Initially not triggered
    assert reminder.is_triggered is False
    assert reminder.status == ReminderStatus.PENDING

    # Trigger the reminder
    reminder.trigger()

    # Verify it's now triggered
    assert reminder.is_triggered is True
    assert reminder.status == ReminderStatus.TRIGGERED


def test_cancel_method():
    """Test the cancel method."""
    future_time = (datetime.now() + timedelta(hours=1)).isoformat()

    reminder = Reminder(
        task_id="task123",
        reminder_time=future_time
    )

    # Initially pending
    assert reminder.status == ReminderStatus.PENDING

    # Cancel the reminder
    reminder.cancel()

    # Verify it's now cancelled
    assert reminder.status == ReminderStatus.CANCELLED


def test_mark_as_missed():
    """Test the mark_as_missed method."""
    future_time = (datetime.now() + timedelta(hours=1)).isoformat()

    reminder = Reminder(
        task_id="task123",
        reminder_time=future_time
    )

    # Initially pending
    assert reminder.status == ReminderStatus.PENDING

    # Mark as missed
    reminder.mark_as_missed()

    # Verify it's now marked as missed
    assert reminder.status == ReminderStatus.MISSED

    # Test with a reminder that has passed time
    reminder2 = Reminder(
        task_id="task456",
        reminder_time=future_time
    )

    # Simulate that time has passed
    past_time = (datetime.now() - timedelta(minutes=1)).isoformat()
    reminder2._reminder_time = past_time  # Bypass validation for testing

    # Mark as missed
    reminder2.mark_as_missed()

    # Verify it's now marked as missed
    assert reminder2.status == ReminderStatus.MISSED


def test_serialization():
    """Test serialization and deserialization of Reminder."""
    future_time = (datetime.now() + timedelta(hours=1)).isoformat()

    original_reminder = Reminder(
        task_id="task123",
        reminder_time=future_time,
        status=ReminderStatus.PENDING
    )

    # Convert to dict
    reminder_dict = original_reminder.to_dict()

    # Convert back from dict
    restored_reminder = Reminder.from_dict(reminder_dict)

    # Verify properties are preserved
    assert restored_reminder.task_id == "task123"
    assert restored_reminder.reminder_time == future_time
    assert restored_reminder.status == ReminderStatus.PENDING
    assert restored_reminder.id == original_reminder.id


def test_string_representation():
    """Test string representations."""
    future_time = (datetime.now() + timedelta(hours=1)).isoformat()

    reminder = Reminder(
        task_id="task123",
        reminder_time=future_time
    )

    str_repr = str(reminder)
    assert "task123" in str_repr
    assert "PENDING" in str_repr.upper()

    repr_repr = repr(reminder)
    assert "task123" in repr_repr
    assert reminder.id in repr_repr


def test_equality():
    """Test equality comparison for Reminder."""
    future_time = (datetime.now() + timedelta(hours=1)).isoformat()

    reminder1 = Reminder(
        task_id="task123",
        reminder_time=future_time
    )

    reminder2 = Reminder(
        task_id="task123",
        reminder_time=future_time
    )

    # Different reminders with same properties should not be equal
    assert reminder1 != reminder2

    # Same reminder (by ID) should be equal - this is tested by assigning same ID
    reminder2._id = reminder1.id
    assert reminder1 == reminder2