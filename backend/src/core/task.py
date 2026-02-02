"""
Task entity for the Todo CLI application.

This module defines the Task class with all required attributes and validation rules
as specified in the data model.
"""
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class TaskStatus(Enum):
    """Enumeration for task status values."""
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"


class TaskPriority(Enum):
    """Enumeration for task priority values."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task:
    """
    Represents a single todo item with all its attributes and metadata.

    Attributes:
        id: Unique identifier (UUID string, required, immutable)
        title: Task title (string, required, 1-200 characters)
        description: Task description (string, optional, 0-1000 characters)
        status: Completion status (enum: "incomplete", "complete", default: "incomplete")
        priority: Task priority level (enum: "low", "medium", "high", default: "medium")
        tags: Array of category tags (string array, optional, 0-10 tags)
        due_date: Optional deadline (ISO 8601 datetime string, optional)
        created_date: Timestamp of creation (ISO 8601 datetime string, required, immutable)
        updated_date: Timestamp of last modification (ISO 8601 datetime string, required, auto-updated)
        recurrence_pattern: Optional recurrence rule (string, optional, for recurring tasks)
    """

    def __init__(
        self,
        title: str,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.INCOMPLETE,
        priority: TaskPriority = TaskPriority.MEDIUM,
        tags: Optional[List[str]] = None,
        due_date: Optional[str] = None,
        id: Optional[str] = None,
        created_date: Optional[str] = None,
        updated_date: Optional[str] = None,
        recurrence_pattern: Optional[str] = None
    ):
        """
        Initialize a Task instance with validation.

        Args:
            title: Task title (1-200 characters)
            description: Task description (0-1000 characters, optional)
            status: Task status (default: incomplete)
            priority: Task priority (default: medium)
            tags: List of tags (0-10 tags, optional)
            due_date: Due date in ISO 8601 format (optional)
            id: Task ID (auto-generated if not provided)
            created_date: Creation timestamp (auto-generated if not provided)
            updated_date: Update timestamp (auto-generated if not provided)
            recurrence_pattern: Recurrence pattern (optional)

        Raises:
            ValueError: If any validation rule is violated
        """
        # Generate ID if not provided
        self._id = id or str(uuid.uuid4())

        # Set creation date if not provided
        self._created_date = created_date or datetime.now().isoformat()

        # Set update date if not provided (or use creation date if provided)
        self._updated_date = updated_date or self._created_date

        # Validate and set title
        self.title = title  # This will use the setter for validation

        # Validate and set description
        self.description = description  # This will use the setter for validation

        # Validate and set status
        self.status = status  # This will use the setter for validation

        # Validate and set priority
        self.priority = priority  # This will use the setter for validation

        # Validate and set tags
        self.tags = tags or []  # This will use the setter for validation

        # Validate and set due date
        self.due_date = due_date  # This will use the setter for validation

        # Validate and set recurrence pattern
        self.recurrence_pattern = recurrence_pattern  # This will use the setter for validation

    @property
    def id(self) -> str:
        """Get the task ID (immutable)."""
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
    def title(self) -> str:
        """Get the task title."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """Set the task title with validation."""
        if not value:
            raise ValueError("Title cannot be empty")
        if len(value) < 1 or len(value) > 200:
            raise ValueError("Title must be between 1 and 200 characters")
        # Update the updated_date when title changes
        if value != getattr(self, '_title', None):
            self._updated_date = datetime.now().isoformat()
        self._title = value

    @property
    def description(self) -> Optional[str]:
        """Get the task description."""
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        """Set the task description with validation."""
        if value is not None:
            if len(value) > 1000:
                raise ValueError("Description must be 1000 characters or less")
        # Update the updated_date when description changes
        if value != getattr(self, '_description', None):
            self._updated_date = datetime.now().isoformat()
        self._description = value

    @property
    def status(self) -> TaskStatus:
        """Get the task status."""
        return self._status

    @status.setter
    def status(self, value: TaskStatus) -> None:
        """Set the task status with validation."""
        if not isinstance(value, TaskStatus):
            raise ValueError("Status must be a TaskStatus enum value")
        # Update the updated_date when status changes
        self._updated_date = datetime.now().isoformat()
        self._status = value

    @property
    def priority(self) -> TaskPriority:
        """Get the task priority."""
        return self._priority

    @priority.setter
    def priority(self, value: TaskPriority) -> None:
        """Set the task priority with validation."""
        if not isinstance(value, TaskPriority):
            raise ValueError("Priority must be a TaskPriority enum value")
        # Update the updated_date when priority changes
        self._updated_date = datetime.now().isoformat()
        self._priority = value

    @property
    def tags(self) -> List[str]:
        """Get the task tags."""
        return self._tags

    @tags.setter
    def tags(self, value: Optional[List[str]]) -> None:
        """Set the task tags with validation."""
        tags = value or []
        if len(tags) > 10:
            raise ValueError("Tasks can have at most 10 tags")
        for tag in tags:
            if not isinstance(tag, str):
                raise ValueError("Tags must be strings")
            if len(tag) > 50:
                raise ValueError("Each tag must be 50 characters or less")
        # Remove duplicates while preserving order
        unique_tags = []
        for tag in tags:
            if tag not in unique_tags:
                unique_tags.append(tag)
        # Update the updated_date when tags change
        self._updated_date = datetime.now().isoformat()
        self._tags = unique_tags

    @property
    def due_date(self) -> Optional[str]:
        """Get the task due date."""
        return self._due_date

    @due_date.setter
    def due_date(self, value: Optional[str]) -> None:
        """Set the task due date with validation."""
        if value is not None:
            self._validate_datetime(value)
        # Update the updated_date when due_date changes
        if value != getattr(self, '_due_date', None):
            self._updated_date = datetime.now().isoformat()
        self._due_date = value

    @property
    def recurrence_pattern(self) -> Optional[str]:
        """Get the task recurrence pattern."""
        return self._recurrence_pattern

    @recurrence_pattern.setter
    def recurrence_pattern(self, value: Optional[str]) -> None:
        """Set the task recurrence pattern."""
        # For now, just store the value - validation will be done by the RecurringTask class
        # Update the updated_date when recurrence_pattern changes
        if value != getattr(self, '_recurrence_pattern', None):
            self._updated_date = datetime.now().isoformat()
        self._recurrence_pattern = value

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

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Task instance to a dictionary representation.

        Returns:
            Dictionary representation of the Task
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "tags": self.tags,
            "due_date": self.due_date,
            "created_date": self.created_date,
            "updated_date": self.updated_date,
            "recurrence_pattern": self.recurrence_pattern
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """
        Create a Task instance from a dictionary representation.

        Args:
            data: Dictionary representation of a Task

        Returns:
            Task instance
        """
        # Convert string values back to enum values
        status = TaskStatus(data['status'])
        priority = TaskPriority(data['priority'])

        return cls(
            id=data['id'],
            title=data['title'],
            description=data.get('description'),
            status=status,
            priority=priority,
            tags=data.get('tags', []),
            due_date=data.get('due_date'),
            created_date=data['created_date'],
            updated_date=data['updated_date'],
            recurrence_pattern=data.get('recurrence_pattern')
        )

    def update(self, **kwargs) -> None:
        """
        Update task attributes with validation.

        Args:
            **kwargs: Task attributes to update
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{key}'")

    def __str__(self) -> str:
        """
        String representation of the Task.

        Returns:
            Human-readable string representation
        """
        status_str = "✓" if self.status == TaskStatus.COMPLETE else "○"
        priority_str = self.priority.value.upper()[0]  # 'H', 'M', 'L'
        tags_str = f" [{', '.join(self.tags)}]" if self.tags else ""
        due_str = f" (due: {self.due_date})" if self.due_date else ""

        return f"{status_str} [{priority_str}] {self.title}{tags_str}{due_str}"

    def __repr__(self) -> str:
        """
        Detailed string representation of the Task.

        Returns:
            Detailed string representation for debugging
        """
        return (f"Task(id='{self.id}', title='{self.title}', status='{self.status.value}', "
                f"priority='{self.priority.value}', tags={self.tags})")

    @classmethod
    def create(cls, title: str, description: Optional[str] = None,
               priority: TaskPriority = TaskPriority.MEDIUM,
               tags: Optional[List[str]] = None, due_date: Optional[str] = None,
               recurrence_pattern: Optional[str] = None) -> 'Task':
        """
        Factory method to create a new Task with a unique ID.

        This method ensures each task gets a unique ID upon creation.

        Args:
            title: Task title (1-200 characters)
            description: Task description (0-1000 characters, optional)
            priority: Task priority (default: medium)
            tags: List of tags (0-10 tags, optional)
            due_date: Due date in ISO 8601 format (optional)
            recurrence_pattern: Recurrence pattern (optional)

        Returns:
            A new Task instance with a unique ID
        """
        return cls(
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date,
            recurrence_pattern=recurrence_pattern
        )

    def __eq__(self, other) -> bool:
        """
        Check equality with another Task instance.

        Args:
            other: Another Task instance to compare with

        Returns:
            True if tasks are equal, False otherwise
        """
        if not isinstance(other, Task):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """
        Hash function for Task instances.

        Returns:
            Hash value based on task ID
        """
        return hash(self.id)