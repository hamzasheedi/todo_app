"""
Reminder entity for the Todo CLI application.

This module defines the Reminder class for time-based notifications.
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List


class ReminderStatus:
    """Class representing reminder status constants."""
    PENDING = "pending"
    TRIGGERED = "triggered"
    MISSED = "missed"
    CANCELLED = "cancelled"


class Reminder:
    """
    Represents a time-based reminder for tasks.

    Attributes:
        id: Unique identifier for the reminder
        task_id: Reference to the associated task
        reminder_time: Scheduled notification time in ISO 8601 format
        is_triggered: Status flag indicating if the reminder has been triggered
        created_date: Timestamp of reminder creation
        updated_date: Timestamp of last modification
        status: Current status of the reminder (pending, triggered, missed, cancelled)
    """

    def __init__(
        self,
        task_id: str,
        reminder_time: str,  # ISO 8601 datetime string
        id: Optional[str] = None,
        is_triggered: bool = False,
        created_date: Optional[str] = None,
        updated_date: Optional[str] = None,
        status: str = ReminderStatus.PENDING
    ):
        """
        Initialize a Reminder instance with validation.

        Args:
            task_id: Reference to the associated task
            reminder_time: Scheduled notification time in ISO 8601 format
            id: Reminder ID (auto-generated if not provided)
            is_triggered: Trigger status (default: False)
            created_date: Creation timestamp (auto-generated if not provided)
            updated_date: Update timestamp (auto-generated if not provided)
            status: Current status of the reminder (default: pending)

        Raises:
            ValueError: If any validation rule is violated
        """
        # Generate ID if not provided
        self._id = id or str(uuid.uuid4())

        # Set creation date if not provided
        self._created_date = created_date or datetime.now().isoformat()

        # Set update date if not provided (or use creation date if provided)
        self._updated_date = updated_date or self._created_date

        # Validate and set task ID
        self.task_id = task_id  # This will use the setter for validation

        # Validate and set reminder time
        self.reminder_time = reminder_time  # This will use the setter for validation

        # Validate and set is_triggered
        self.is_triggered = is_triggered  # This will use the setter for validation

        # Validate and set status
        self.status = status  # This will use the setter for validation

    @property
    def id(self) -> str:
        """Get the reminder ID (immutable)."""
        return self._id

    @property
    def created_date(self) -> str:
        """Get the creation date (immutable)."""
        return self._created_date

    @property
    def updated_date(self) -> str:
        """Get the last update date."""
        return self._updated_date

    @updated_date.setter
    def updated_date(self, value: str) -> None:
        """Set the update date (used internally)."""
        self._validate_datetime(value)
        self._updated_date = value

    @property
    def task_id(self) -> str:
        """Get the associated task ID."""
        return self._task_id

    @task_id.setter
    def task_id(self, value: str) -> None:
        """Set the associated task ID with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Task ID must be a non-empty string")
        if len(value) > 100:  # Reasonable length limit
            raise ValueError("Task ID is too long (max 100 characters)")
        # Update the updated_date when task_id changes
        self._updated_date = datetime.now().isoformat()
        self._task_id = value

    @property
    def reminder_time(self) -> str:
        """Get the reminder time."""
        return self._reminder_time

    @reminder_time.setter
    def reminder_time(self, value: str) -> None:
        """Set the reminder time with validation."""
        self._validate_datetime(value)
        # Check that it's a future time
        reminder_dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if reminder_dt < datetime.now():
            raise ValueError("Reminder time must be in the future")
        # Update the updated_date when reminder_time changes
        self._updated_date = datetime.now().isoformat()
        self._reminder_time = value

    @property
    def is_triggered(self) -> bool:
        """Get the triggered status."""
        return self._is_triggered

    @is_triggered.setter
    def is_triggered(self, value: bool) -> None:
        """Set the triggered status with validation."""
        if not isinstance(value, bool):
            raise ValueError("is_triggered must be a boolean")
        # Update the updated_date when is_triggered changes
        self._updated_date = datetime.now().isoformat()
        self._is_triggered = value

    @property
    def status(self) -> str:
        """Get the reminder status."""
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        """Set the reminder status with validation."""
        valid_statuses = [ReminderStatus.PENDING, ReminderStatus.TRIGGERED,
                         ReminderStatus.MISSED, ReminderStatus.CANCELLED]
        if value not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        # Update the updated_date when status changes
        self._updated_date = datetime.now().isoformat()
        self._status = value

    def _validate_datetime(self, datetime_str: str) -> None:
        """
        Validate that a string is in ISO 8601 datetime format.

        Args:
            datetime_str: String to validate as ISO 8601 datetime

        Raises:
            ValueError: If the string is not in valid ISO 8601 format
        """
        try:
            datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError(f"Invalid ISO 8601 datetime format: {datetime_str}")

    def is_overdue(self) -> bool:
        """
        Check if the reminder is overdue (should have been triggered).

        Returns:
            True if the reminder time has passed and it hasn't been triggered, False otherwise
        """
        reminder_dt = datetime.fromisoformat(self.reminder_time.replace('Z', '+00:00'))
        return datetime.now() > reminder_dt and not self.is_triggered

    def should_trigger(self) -> bool:
        """
        Determine if the reminder should be triggered now.

        Returns:
            True if the reminder should be triggered, False otherwise
        """
        if self.status != ReminderStatus.PENDING:
            return False

        reminder_dt = datetime.fromisoformat(self.reminder_time.replace('Z', '+00:00'))
        now = datetime.now()

        # Check if it's time to trigger (within a reasonable window to account for timing differences)
        # For simplicity, we'll say it should trigger if the reminder time has passed
        # and it hasn't been triggered yet
        return reminder_dt <= now and not self.is_triggered

    def trigger(self) -> None:
        """
        Mark the reminder as triggered and update its status.
        """
        self.is_triggered = True
        self.status = ReminderStatus.TRIGGERED
        self._updated_date = datetime.now().isoformat()

    def cancel(self) -> None:
        """
        Cancel the reminder and update its status.
        """
        self.status = ReminderStatus.CANCELLED
        self._updated_date = datetime.now().isoformat()

    def mark_as_missed(self) -> None:
        """
        Mark the reminder as missed and update its status.
        """
        self.status = ReminderStatus.MISSED
        self._updated_date = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Reminder instance to a dictionary representation.

        Returns:
            Dictionary representation of the Reminder
        """
        return {
            "id": self.id,
            "task_id": self.task_id,
            "reminder_time": self.reminder_time,
            "is_triggered": self.is_triggered,
            "created_date": self.created_date,
            "updated_date": self.updated_date,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Reminder':
        """
        Create a Reminder instance from a dictionary representation.

        Args:
            data: Dictionary representation of a Reminder

        Returns:
            Reminder instance
        """
        return cls(
            id=data['id'],
            task_id=data['task_id'],
            reminder_time=data['reminder_time'],
            is_triggered=data.get('is_triggered', False),
            created_date=data['created_date'],
            updated_date=data['updated_date'],
            status=data.get('status', ReminderStatus.PENDING)
        )

    def __str__(self) -> str:
        """
        String representation of the Reminder.

        Returns:
            Human-readable string representation
        """
        status_str = "TRIGGERED" if self.is_triggered else self.status.upper()
        return f"Reminder for task {self.task_id} at {self.reminder_time} ({status_str})"

    def __repr__(self) -> str:
        """
        Detailed string representation of the Reminder.

        Returns:
            Detailed string representation for debugging
        """
        return (f"Reminder(id='{self.id}', task_id='{self.task_id}', "
                f"reminder_time='{self.reminder_time}', status='{self.status}')")

    def __eq__(self, other) -> bool:
        """
        Check equality with another Reminder instance.

        Args:
            other: Another Reminder instance to compare with

        Returns:
            True if reminders are equal, False otherwise
        """
        if not isinstance(other, Reminder):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """
        Hash function for Reminder instances.

        Returns:
            Hash value based on reminder ID
        """
        return hash(self.id)


class ReminderManager:
    """
    Manager class for handling reminders and their scheduling.
    """

    def __init__(self):
        """Initialize the reminder manager."""
        self.reminders = []

    def add_reminder(self, reminder: Reminder) -> None:
        """
        Add a reminder to the manager.

        Args:
            reminder: Reminder instance to add
        """
        self.reminders.append(reminder)

    def remove_reminder(self, reminder_id: str) -> bool:
        """
        Remove a reminder from the manager.

        Args:
            reminder_id: ID of the reminder to remove

        Returns:
            True if the reminder was found and removed, False otherwise
        """
        for i, r in enumerate(self.reminders):
            if r.id == reminder_id:
                del self.reminders[i]
                return True
        return False

    def get_reminder(self, reminder_id: str) -> Optional[Reminder]:
        """
        Get a reminder by ID.

        Args:
            reminder_id: ID of the reminder to retrieve

        Returns:
            Reminder instance if found, None otherwise
        """
        for r in self.reminders:
            if r.id == reminder_id:
                return r
        return None

    def get_pending_reminders(self) -> list[Reminder]:
        """
        Get all pending reminders.

        Returns:
            List of Reminder instances with status 'pending'
        """
        return [r for r in self.reminders if r.status == ReminderStatus.PENDING]

    def get_reminders_for_task(self, task_id: str) -> list[Reminder]:
        """
        Get all reminders for a specific task.

        Args:
            task_id: ID of the task

        Returns:
            List of Reminder instances for the task
        """
        return [r for r in self.reminders if r.task_id == task_id]

    def get_due_reminders(self) -> list[Reminder]:
        """
        Get all reminders that are due for triggering.

        Returns:
            List of Reminder instances that should be triggered now
        """
        due_reminders = []
        for r in self.reminders:
            if r.should_trigger():
                due_reminders.append(r)
        return due_reminders

    def process_due_reminders(self) -> list[Reminder]:
        """
        Process all due reminders by triggering them.

        Returns:
            List of triggered Reminder instances
        """
        triggered_reminders = []
        due_reminders = self.get_due_reminders()

        for reminder in due_reminders:
            if not reminder.is_triggered:
                reminder.trigger()
                triggered_reminders.append(reminder)

        return triggered_reminders

    def cancel_reminder(self, reminder_id: str) -> bool:
        """
        Cancel a reminder.

        Args:
            reminder_id: ID of the reminder to cancel

        Returns:
            True if the reminder was found and cancelled, False otherwise
        """
        reminder = self.get_reminder(reminder_id)
        if reminder:
            reminder.cancel()
            return True
        return False

    def mark_reminders_as_missed(self) -> int:
        """
        Mark all overdue reminders as missed.

        Returns:
            Number of reminders marked as missed
        """
        missed_count = 0
        for reminder in self.reminders:
            if reminder.status == ReminderStatus.PENDING and reminder.is_overdue():
                reminder.mark_as_missed()
                missed_count += 1
        return missed_count

    def get_upcoming_reminders(self, hours: int = 24) -> list[Reminder]:
        """
        Get all reminders scheduled within the next specified hours.

        Args:
            hours: Number of hours to look ahead (default: 24)

        Returns:
            List of upcoming Reminder instances
        """
        from datetime import timedelta
        future_time = (datetime.now() + timedelta(hours=hours)).isoformat()

        upcoming = []
        for reminder in self.reminders:
            if (reminder.status == ReminderStatus.PENDING and
                reminder.reminder_time <= future_time):
                upcoming.append(reminder)
        return upcoming