"""
Tests for the ReminderManager class.
"""
from datetime import datetime, timedelta
from src.core.reminder import Reminder, ReminderManager, ReminderStatus


def test_reminder_manager():
    """Test basic ReminderManager functionality."""
    manager = ReminderManager()

    future_time = (datetime.now() + timedelta(hours=1)).isoformat()

    # Create a reminder
    reminder = Reminder(
        task_id="task123",
        reminder_time=future_time
    )

    # Add the reminder to the manager
    manager.add_reminder(reminder)

    # Verify it was added
    assert len(manager.reminders) == 1
    assert manager.get_reminder(reminder.id) == reminder

    # Get all pending reminders
    pending = manager.get_pending_reminders()
    assert len(pending) == 1
    assert pending[0].id == reminder.id

    # Get reminders for a specific task
    task_reminders = manager.get_reminders_for_task("task123")
    assert len(task_reminders) == 1
    assert task_reminders[0].id == reminder.id

    # Test removing a reminder
    result = manager.remove_reminder(reminder.id)
    assert result is True
    assert len(manager.reminders) == 0

    # Try to remove a non-existent reminder
    result = manager.remove_reminder("non-existent")
    assert result is False


def test_get_due_reminders():
    """Test getting due reminders."""
    manager = ReminderManager()

    future_time1 = (datetime.now() + timedelta(hours=1)).isoformat()
    future_time2 = (datetime.now() + timedelta(hours=2)).isoformat()

    # Create reminders with future times initially
    due_reminder = Reminder(
        task_id="task123",
        reminder_time=future_time1
    )

    future_reminder = Reminder(
        task_id="task456",
        reminder_time=future_time2
    )

    manager.add_reminder(due_reminder)
    manager.add_reminder(future_reminder)

    # Directly modify the internal time for testing to simulate past time
    past_time = (datetime.now() - timedelta(minutes=1)).isoformat()
    due_reminder._reminder_time = past_time  # Make it past time to simulate being due

    # Get due reminders
    due_reminders = manager.get_due_reminders()
    assert len(due_reminders) == 1
    assert due_reminders[0].id == due_reminder.id


def test_process_due_reminders():
    """Test processing due reminders."""
    manager = ReminderManager()

    future_time1 = (datetime.now() + timedelta(hours=1)).isoformat()
    future_time2 = (datetime.now() + timedelta(hours=2)).isoformat()

    # Create reminders with future times initially
    due_reminder = Reminder(
        task_id="task123",
        reminder_time=future_time1
    )

    future_reminder = Reminder(
        task_id="task456",
        reminder_time=future_time2
    )

    manager.add_reminder(due_reminder)
    manager.add_reminder(future_reminder)

    # Simulate that time has passed for due_reminder
    past_time = (datetime.now() - timedelta(minutes=1)).isoformat()
    due_reminder._reminder_time = past_time  # Bypass validation for testing

    # Process due reminders
    triggered = manager.process_due_reminders()
    assert len(triggered) == 1
    assert triggered[0].id == due_reminder.id
    assert due_reminder.is_triggered is True
    assert due_reminder.status == ReminderStatus.TRIGGERED


def test_cancel_reminder():
    """Test cancelling a reminder."""
    manager = ReminderManager()

    future_time = (datetime.now() + timedelta(hours=1)).isoformat()

    # Create a reminder
    reminder = Reminder(
        task_id="task123",
        reminder_time=future_time
    )

    manager.add_reminder(reminder)

    # Verify it's pending
    assert reminder.status == ReminderStatus.PENDING

    # Cancel the reminder
    result = manager.cancel_reminder(reminder.id)
    assert result is True
    assert reminder.status == ReminderStatus.CANCELLED

    # Try to cancel a non-existent reminder
    result = manager.cancel_reminder("non-existent")
    assert result is False


def test_mark_reminders_as_missed():
    """Test marking overdue reminders as missed."""
    manager = ReminderManager()

    future_time1 = (datetime.now() + timedelta(hours=1)).isoformat()
    future_time2 = (datetime.now() + timedelta(hours=2)).isoformat()

    # Create reminders with future times initially
    overdue_reminder = Reminder(
        task_id="task123",
        reminder_time=future_time1
    )

    future_reminder = Reminder(
        task_id="task456",
        reminder_time=future_time2
    )

    manager.add_reminder(overdue_reminder)
    manager.add_reminder(future_reminder)

    # Simulate that time has passed for overdue_reminder
    past_time = (datetime.now() - timedelta(minutes=1)).isoformat()
    overdue_reminder._reminder_time = past_time  # Bypass validation for testing

    # Mark reminders as missed
    missed_count = manager.mark_reminders_as_missed()
    assert missed_count == 1
    assert overdue_reminder.status == ReminderStatus.MISSED
    assert future_reminder.status == ReminderStatus.PENDING  # Should remain unchanged


def test_get_upcoming_reminders():
    """Test getting upcoming reminders."""
    manager = ReminderManager()

    # Times for testing
    now = datetime.now()
    near_future_time = (now + timedelta(minutes=30)).isoformat()
    far_future_time = (now + timedelta(hours=25)).isoformat()  # More than 24 hours
    another_near_time = (now + timedelta(minutes=45)).isoformat()

    # Create reminders at different times
    near_reminder = Reminder(
        task_id="task123",
        reminder_time=near_future_time
    )

    far_reminder = Reminder(
        task_id="task456",
        reminder_time=far_future_time
    )

    another_near_reminder = Reminder(
        task_id="task789",
        reminder_time=another_near_time
    )

    manager.add_reminder(near_reminder)
    manager.add_reminder(far_reminder)
    manager.add_reminder(another_near_reminder)

    # Get upcoming reminders within 24 hours
    # far_reminder should not be included as it's beyond 24 hours
    upcoming = manager.get_upcoming_reminders(24)
    assert len(upcoming) == 2  # near_reminder and another_near_reminder

    upcoming_ids = [r.id for r in upcoming]
    assert near_reminder.id in upcoming_ids
    assert another_near_reminder.id in upcoming_ids
    assert far_reminder.id not in upcoming_ids


def test_multiple_reminders_same_task():
    """Test multiple reminders for the same task."""
    manager = ReminderManager()

    future_time1 = (datetime.now() + timedelta(hours=1)).isoformat()
    future_time2 = (datetime.now() + timedelta(hours=2)).isoformat()

    # Create multiple reminders for the same task
    reminder1 = Reminder(
        task_id="task123",
        reminder_time=future_time1
    )

    reminder2 = Reminder(
        task_id="task123",
        reminder_time=future_time2
    )

    manager.add_reminder(reminder1)
    manager.add_reminder(reminder2)

    # Get reminders for the task
    task_reminders = manager.get_reminders_for_task("task123")
    assert len(task_reminders) == 2

    task_ids = [r.id for r in task_reminders]
    assert reminder1.id in task_ids
    assert reminder2.id in task_ids


def test_reminder_lifecycle():
    """Test a complete reminder lifecycle."""
    manager = ReminderManager()

    future_time = (datetime.now() + timedelta(hours=1)).isoformat()

    # Create a reminder
    reminder = Reminder(
        task_id="task123",
        reminder_time=future_time
    )

    manager.add_reminder(reminder)

    # Initially pending
    assert reminder.status == ReminderStatus.PENDING

    # Simulate time passing
    past_time = (datetime.now() - timedelta(minutes=1)).isoformat()
    reminder._reminder_time = past_time  # Bypass validation for testing

    # Check if it's due
    due_reminders = manager.get_due_reminders()
    assert len(due_reminders) == 1
    assert due_reminders[0].id == reminder.id

    # Process the due reminder
    triggered = manager.process_due_reminders()
    assert len(triggered) == 1
    assert triggered[0].id == reminder.id
    assert reminder.is_triggered is True
    assert reminder.status == ReminderStatus.TRIGGERED