"""
RecurringTask entity for the Todo CLI application.

This module defines the RecurringTask class for managing recurring tasks.
"""
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Dict, Any, List
from core.task import Task


class RecurrenceRule(Enum):
    """Enumeration for recurrence rules."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class ContinuePolicy(Enum):
    """Enumeration for continuation policies after task completion."""
    ALWAYS_CONTINUE = "always_continue"
    PROMPT_USER = "prompt_user"
    STOP_IF_COMPLETED = "stop_if_completed"


class RecurringTask:
    """
    Represents a recurring task with scheduling and generation capabilities.

    Attributes:
        id: Unique identifier for the recurring task
        base_task: Template task that defines the recurring task properties
        recurrence_rule: Frequency pattern (daily, weekly, monthly, yearly)
        next_occurrence: Next scheduled occurrence datetime
        is_active: Enable/disable flag
        end_date: Optional end date for recurrence
        continue_after_completion: Policy for continuing recurrence after task completion
        created_date: Timestamp of creation
        updated_date: Timestamp of last modification
    """

    def __init__(
        self,
        base_task: Task,
        recurrence_rule: RecurrenceRule,
        next_occurrence: str,  # ISO 8601 datetime string
        is_active: bool = True,
        end_date: Optional[str] = None,  # ISO 8601 datetime string
        continue_after_completion: ContinuePolicy = ContinuePolicy.ALWAYS_CONTINUE,
        id: Optional[str] = None,
        created_date: Optional[str] = None,
        updated_date: Optional[str] = None
    ):
        """
        Initialize a RecurringTask instance with validation.

        Args:
            base_task: Template task that defines the recurring task properties
            recurrence_rule: Frequency pattern (daily, weekly, monthly, yearly)
            next_occurrence: Next scheduled occurrence datetime in ISO 8601 format
            is_active: Enable/disable flag (default: True)
            end_date: Optional end date for recurrence in ISO 8601 format
            continue_after_completion: Policy for continuing after completion (default: ALWAYS_CONTINUE)
            id: Recurring task ID (auto-generated if not provided)
            created_date: Creation timestamp (auto-generated if not provided)
            updated_date: Update timestamp (auto-generated if not provided)

        Raises:
            ValueError: If any validation rule is violated
        """
        # Generate ID if not provided
        self._id = id or str(uuid.uuid4())

        # Set creation date if not provided
        self._created_date = created_date or datetime.now().isoformat()

        # Set update date if not provided (or use creation date if provided)
        self._updated_date = updated_date or self._created_date

        # Validate and set base task
        self.base_task = base_task  # This will use the setter for validation

        # Validate and set recurrence rule
        self.recurrence_rule = recurrence_rule  # This will use the setter for validation

        # Validate and set next occurrence
        self.next_occurrence = next_occurrence  # This will use the setter for validation

        # Validate and set is_active
        self.is_active = is_active  # This will use the setter for validation

        # Validate and set end date
        self.end_date = end_date  # This will use the setter for validation

        # Validate and set continue_after_completion
        self.continue_after_completion = continue_after_completion  # This will use the setter for validation

    @property
    def id(self) -> str:
        """Get the recurring task ID (immutable)."""
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
    def base_task(self) -> Task:
        """Get the base task template."""
        return self._base_task

    @base_task.setter
    def base_task(self, value: Task) -> None:
        """Set the base task template."""
        if not isinstance(value, Task):
            raise ValueError("Base task must be a Task instance")
        self._base_task = value

    @property
    def recurrence_rule(self) -> RecurrenceRule:
        """Get the recurrence rule."""
        return self._recurrence_rule

    @recurrence_rule.setter
    def recurrence_rule(self, value: RecurrenceRule) -> None:
        """Set the recurrence rule with validation."""
        if not isinstance(value, RecurrenceRule):
            raise ValueError("Recurrence rule must be a RecurrenceRule enum value")
        # Update the updated_date when recurrence rule changes
        self._updated_date = datetime.now().isoformat()
        self._recurrence_rule = value

    @property
    def next_occurrence(self) -> str:
        """Get the next occurrence date."""
        return self._next_occurrence

    @next_occurrence.setter
    def next_occurrence(self, value: str) -> None:
        """Set the next occurrence date with validation."""
        self._validate_datetime(value)
        # Check that it's a future date
        next_dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if next_dt < datetime.now():
            raise ValueError("Next occurrence must be in the future")
        # Update the updated_date when next occurrence changes
        self._updated_date = datetime.now().isoformat()
        self._next_occurrence = value

    @property
    def is_active(self) -> bool:
        """Get the active status."""
        return self._is_active

    @is_active.setter
    def is_active(self, value: bool) -> None:
        """Set the active status with validation."""
        if not isinstance(value, bool):
            raise ValueError("Active status must be a boolean")
        # Update the updated_date when active status changes
        self._updated_date = datetime.now().isoformat()
        self._is_active = value

    @property
    def end_date(self) -> Optional[str]:
        """Get the end date."""
        return self._end_date

    @end_date.setter
    def end_date(self, value: Optional[str]) -> None:
        """Set the end date with validation."""
        if value is not None:
            self._validate_datetime(value)
            # Check that end date is after next occurrence
            end_dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
            next_dt = datetime.fromisoformat(self._next_occurrence.replace('Z', '+00:00'))
            if end_dt < next_dt:
                raise ValueError("End date must be after next occurrence")
        # Update the updated_date when end date changes
        if value != getattr(self, '_end_date', None):
            self._updated_date = datetime.now().isoformat()
        self._end_date = value

    @property
    def continue_after_completion(self) -> ContinuePolicy:
        """Get the continue after completion policy."""
        return self._continue_after_completion

    @continue_after_completion.setter
    def continue_after_completion(self, value: ContinuePolicy) -> None:
        """Set the continue after completion policy with validation."""
        if not isinstance(value, ContinuePolicy):
            raise ValueError("Continue after completion must be a ContinuePolicy enum value")
        # Update the updated_date when policy changes
        self._updated_date = datetime.now().isoformat()
        self._continue_after_completion = value

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

    def calculate_next_occurrence(self) -> str:
        """
        Calculate the next occurrence based on the recurrence rule.

        Returns:
            ISO 8601 datetime string for the next occurrence
        """
        current_dt = datetime.fromisoformat(self.next_occurrence.replace('Z', '+00:00'))

        if self.recurrence_rule == RecurrenceRule.DAILY:
            next_dt = current_dt + timedelta(days=1)
        elif self.recurrence_rule == RecurrenceRule.WEEKLY:
            next_dt = current_dt + timedelta(weeks=1)
        elif self.recurrence_rule == RecurrenceRule.MONTHLY:
            # For monthly recurrence, we add 1 month (approximately 30 days)
            # In a real application, this would need more sophisticated handling
            next_dt = current_dt + timedelta(days=30)
        elif self.recurrence_rule == RecurrenceRule.YEARLY:
            next_dt = current_dt + timedelta(days=365)
        else:
            raise ValueError(f"Unknown recurrence rule: {self.recurrence_rule}")

        return next_dt.isoformat()

    def should_generate_new_task(self) -> bool:
        """
        Determine if a new task instance should be generated.

        Returns:
            True if a new task should be generated, False otherwise
        """
        if not self.is_active:
            return False

        # Check if current time is past the next occurrence
        next_dt = datetime.fromisoformat(self.next_occurrence.replace('Z', '+00:00'))
        if datetime.now() < next_dt:
            return False

        # Check if we've reached the end date (if specified)
        if self.end_date:
            end_dt = datetime.fromisoformat(self.end_date.replace('Z', '+00:00'))
            if datetime.now() >= end_dt:
                return False

        return True

    def generate_task_instance(self) -> Task:
        """
        Generate a new task instance based on the base task template.

        Returns:
            A new Task instance with updated dates and unique ID
        """
        # Create a new task based on the base task
        new_task = Task(
            title=self.base_task.title,
            description=self.base_task.description,
            status=self.base_task.status,  # Start with incomplete status
            priority=self.base_task.priority,
            tags=self.base_task.tags,
            due_date=self.base_task.due_date,
            # Generate a new unique ID for the instance
            id=str(uuid.uuid4()),
            created_date=datetime.now().isoformat(),
            updated_date=datetime.now().isoformat(),
            recurrence_pattern=self.recurrence_rule.value
        )

        return new_task

    def update_next_occurrence(self) -> None:
        """
        Update the next occurrence to the calculated next occurrence.
        """
        self.next_occurrence = self.calculate_next_occurrence()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the RecurringTask instance to a dictionary representation.

        Returns:
            Dictionary representation of the RecurringTask
        """
        return {
            "id": self.id,
            "base_task": self.base_task.to_dict(),
            "recurrence_rule": self.recurrence_rule.value,
            "next_occurrence": self.next_occurrence,
            "is_active": self.is_active,
            "end_date": self.end_date,
            "continue_after_completion": self.continue_after_completion.value,
            "created_date": self.created_date,
            "updated_date": self.updated_date
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RecurringTask':
        """
        Create a RecurringTask instance from a dictionary representation.

        Args:
            data: Dictionary representation of a RecurringTask

        Returns:
            RecurringTask instance
        """
        from core.task import Task  # Import here to avoid circular dependency

        # Convert string values back to enum values
        recurrence_rule = RecurrenceRule(data['recurrence_rule'])
        continue_policy = ContinuePolicy(data['continue_after_completion'])

        # Create base task from dictionary
        base_task = Task.from_dict(data['base_task'])

        return cls(
            id=data['id'],
            base_task=base_task,
            recurrence_rule=recurrence_rule,
            next_occurrence=data['next_occurrence'],
            is_active=data['is_active'],
            end_date=data.get('end_date'),
            continue_after_completion=continue_policy,
            created_date=data['created_date'],
            updated_date=data['updated_date']
        )

    def __str__(self) -> str:
        """
        String representation of the RecurringTask.

        Returns:
            Human-readable string representation
        """
        status_str = "Active" if self.is_active else "Inactive"
        return f"RecurringTask: {self.base_task.title} ({self.recurrence_rule.value}, {status_str})"

    def __repr__(self) -> str:
        """
        Detailed string representation of the RecurringTask.

        Returns:
            Detailed string representation for debugging
        """
        return (f"RecurringTask(id='{self.id}', title='{self.base_task.title}', "
                f"rule='{self.recurrence_rule.value}', active={self.is_active})")

    def __eq__(self, other) -> bool:
        """
        Check equality with another RecurringTask instance.

        Args:
            other: Another RecurringTask instance to compare with

        Returns:
            True if recurring tasks are equal, False otherwise
        """
        if not isinstance(other, RecurringTask):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """
        Hash function for RecurringTask instances.

        Returns:
            Hash value based on recurring task ID
        """
        return hash(self.id)


class RecurringTaskManager:
    """
    Manager class for handling recurring tasks and their scheduling.
    """

    def __init__(self):
        """Initialize the recurring task manager."""
        self.recurring_tasks = []

    def add_recurring_task(self, recurring_task: RecurringTask) -> None:
        """
        Add a recurring task to the manager.

        Args:
            recurring_task: RecurringTask instance to add
        """
        self.recurring_tasks.append(recurring_task)

    def remove_recurring_task(self, recurring_task_id: str) -> bool:
        """
        Remove a recurring task from the manager.

        Args:
            recurring_task_id: ID of the recurring task to remove

        Returns:
            True if the recurring task was found and removed, False otherwise
        """
        for i, rt in enumerate(self.recurring_tasks):
            if rt.id == recurring_task_id:
                del self.recurring_tasks[i]
                return True
        return False

    def get_recurring_task(self, recurring_task_id: str) -> Optional[RecurringTask]:
        """
        Get a recurring task by ID.

        Args:
            recurring_task_id: ID of the recurring task to retrieve

        Returns:
            RecurringTask instance if found, None otherwise
        """
        for rt in self.recurring_tasks:
            if rt.id == recurring_task_id:
                return rt
        return None

    def get_tasks_to_generate(self) -> list[RecurringTask]:
        """
        Get all recurring tasks that should generate new instances.

        Returns:
            List of RecurringTask instances that should generate new tasks
        """
        tasks_to_generate = []
        for rt in self.recurring_tasks:
            if rt.should_generate_new_task():
                tasks_to_generate.append(rt)
        return tasks_to_generate

    def process_recurring_tasks(self) -> list[Task]:
        """
        Process all recurring tasks and generate new task instances as needed.

        This method checks all recurring tasks and generates new task instances
        for those that are due, updating their next occurrence as appropriate.

        Returns:
            List of newly generated Task instances
        """
        new_tasks = []

        for recurring_task in self.recurring_tasks:
            if recurring_task.should_generate_new_task():
                # Generate a new task instance
                new_task = recurring_task.generate_task_instance()
                new_tasks.append(new_task)

                # Update the next occurrence for the recurring task
                recurring_task.update_next_occurrence()

                # Check the continuation policy
                if recurring_task.continue_after_completion == ContinuePolicy.STOP_IF_COMPLETED:
                    # This implementation would need to track task completion status
                    # For now, we'll continue as normal
                    pass
                elif recurring_task.continue_after_completion == ContinuePolicy.PROMPT_USER:
                    # In a real application, this would prompt the user
                    # For now, we'll continue as normal
                    pass
                # ALWAYS_CONTINUE continues automatically

        return new_tasks

    def disable_recurring_task(self, recurring_task_id: str) -> bool:
        """
        Disable a recurring task (set is_active to False).

        Args:
            recurring_task_id: ID of the recurring task to disable

        Returns:
            True if the recurring task was found and disabled, False otherwise
        """
        recurring_task = self.get_recurring_task(recurring_task_id)
        if recurring_task:
            recurring_task.is_active = False
            return True
        return False

    def enable_recurring_task(self, recurring_task_id: str) -> bool:
        """
        Enable a recurring task (set is_active to True).

        Args:
            recurring_task_id: ID of the recurring task to enable

        Returns:
            True if the recurring task was found and enabled, False otherwise
        """
        recurring_task = self.get_recurring_task(recurring_task_id)
        if recurring_task:
            recurring_task.is_active = True
            return True
        return False