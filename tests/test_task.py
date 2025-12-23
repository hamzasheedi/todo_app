"""
Tests for the Task entity class.
"""
import pytest
from datetime import datetime
from src.core.task import Task, TaskStatus, TaskPriority


def test_task_creation_basic():
    """Test basic task creation with required fields."""
    task = Task(title="Test Task")

    assert task.title == "Test Task"
    assert task.status == TaskStatus.INCOMPLETE
    assert task.priority == TaskPriority.MEDIUM
    assert task.tags == []
    assert task.description is None
    assert task.due_date is None
    assert task.id is not None
    assert task.created_date is not None
    assert task.updated_date is not None


def test_task_creation_with_all_fields():
    """Test task creation with all fields."""
    due_date = "2025-12-31T10:00:00"
    task = Task(
        title="Complete Project",
        description="Finish the todo app project",
        status=TaskStatus.COMPLETE,
        priority=TaskPriority.HIGH,
        tags=["work", "urgent"],
        due_date=due_date
    )

    assert task.title == "Complete Project"
    assert task.description == "Finish the todo app project"
    assert task.status == TaskStatus.COMPLETE
    assert task.priority == TaskPriority.HIGH
    assert task.tags == ["work", "urgent"]
    assert task.due_date == due_date


def test_task_title_validation():
    """Test title validation rules."""
    # Test empty title
    with pytest.raises(ValueError, match="Title cannot be empty"):
        Task(title="")

    # Test title too short (this shouldn't happen as empty is caught above)
    # Test title too long
    long_title = "x" * 201
    with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
        Task(title=long_title)

    # Test valid title at boundary
    valid_title = "x" * 200
    task = Task(title=valid_title)
    assert task.title == valid_title


def test_task_description_validation():
    """Test description validation rules."""
    # Test description too long
    long_description = "x" * 1001
    with pytest.raises(ValueError, match="Description must be 1000 characters or less"):
        Task(title="Test", description=long_description)

    # Test valid description at boundary
    valid_description = "x" * 1000
    task = Task(title="Test", description=valid_description)
    assert task.description == valid_description


def test_task_status_validation():
    """Test status validation."""
    # Test valid statuses
    task = Task(title="Test")
    task.status = TaskStatus.COMPLETE
    assert task.status == TaskStatus.COMPLETE

    # Test invalid status type
    task = Task(title="Test")
    with pytest.raises(ValueError, match="Status must be a TaskStatus enum value"):
        task.status = "invalid"


def test_task_priority_validation():
    """Test priority validation."""
    # Test valid priorities
    task = Task(title="Test")
    task.priority = TaskPriority.LOW
    assert task.priority == TaskPriority.LOW

    # Test invalid priority type
    task = Task(title="Test")
    with pytest.raises(ValueError, match="Priority must be a TaskPriority enum value"):
        task.priority = "invalid"


def test_task_tags_validation():
    """Test tags validation."""
    # Test too many tags
    with pytest.raises(ValueError, match="Tasks can have at most 10 tags"):
        Task(title="Test", tags=["tag" + str(i) for i in range(11)])

    # Test tag too long
    with pytest.raises(ValueError, match="Each tag must be 50 characters or less"):
        Task(title="Test", tags=["x" * 51])

    # Test duplicate tags are removed
    task = Task(title="Test", tags=["work", "urgent", "work"])
    assert task.tags == ["work", "urgent"]  # Duplicates removed, order preserved


def test_task_due_date_validation():
    """Test due date validation."""
    # Test invalid date format
    with pytest.raises(ValueError, match="Invalid ISO 8601 datetime format"):
        Task(title="Test", due_date="invalid-date-format")

    # Test valid date formats
    valid_dates = [
        "2025-12-31T10:00:00",
        "2025-12-31T10:00:00Z",
        "2025-12-31T10:00:00+00:00",
        "2025-12-31",
    ]

    for date_str in valid_dates:
        task = Task(title="Test", due_date=date_str)
        assert task.due_date == date_str


def test_task_update_method():
    """Test the update method."""
    task = Task(title="Original Title")

    # Update multiple fields
    task.update(
        title="Updated Title",
        description="Updated Description",
        priority=TaskPriority.HIGH
    )

    assert task.title == "Updated Title"
    assert task.description == "Updated Description"
    assert task.priority == TaskPriority.HIGH


def test_task_to_dict_and_from_dict():
    """Test serialization and deserialization."""
    original_task = Task(
        title="Serialization Test",
        description="Test task for serialization",
        status=TaskStatus.COMPLETE,
        priority=TaskPriority.HIGH,
        tags=["test", "serialization"],
        due_date="2025-12-31T10:00:00"
    )

    # Convert to dict
    task_dict = original_task.to_dict()

    # Convert back from dict
    restored_task = Task.from_dict(task_dict)

    # Check that all values match
    assert restored_task.title == original_task.title
    assert restored_task.description == original_task.description
    assert restored_task.status == original_task.status
    assert restored_task.priority == original_task.priority
    assert restored_task.tags == original_task.tags
    assert restored_task.due_date == original_task.due_date
    assert restored_task.id == original_task.id
    assert restored_task.created_date == original_task.created_date


def test_task_string_representation():
    """Test string representations."""
    task = Task(
        title="Test Task",
        priority=TaskPriority.HIGH,
        tags=["work", "urgent"],
        due_date="2025-12-31T10:00:00"
    )

    str_repr = str(task)
    assert "○" in str_repr  # Incomplete status
    assert "[H]" in str_repr  # High priority
    assert "Test Task" in str_repr
    assert "work, urgent" in str_repr
    assert "due: 2025-12-31T10:00:00" in str_repr

    # Test completed task
    task.status = TaskStatus.COMPLETE
    str_repr_complete = str(task)
    assert "✓" in str_repr_complete  # Complete status


def test_task_equality():
    """Test task equality based on ID."""
    task1 = Task(title="Test 1")
    task2 = Task(title="Test 2")
    task3 = Task(title="Test 3")

    # Same ID should be equal
    task3._id = task1.id  # Manually set same ID for testing
    assert task1 == task3

    # Different IDs should not be equal
    assert task1 != task2


def test_updated_date_changes():
    """Test that updated_date changes when fields are modified."""
    task = Task(title="Original")
    original_updated = task.updated_date

    # Wait a moment to ensure time difference
    import time
    time.sleep(0.01)

    # Change a field
    task.title = "Updated Title"

    # Updated date should be different
    assert task.updated_date != original_updated

    # Change status
    original_updated = task.updated_date
    time.sleep(0.01)
    task.status = TaskStatus.COMPLETE
    assert task.updated_date != original_updated


def test_task_factory_method():
    """Test the Task factory method for creating tasks with unique IDs."""
    # Create a task using the factory method
    task = Task.create(title="Factory Task", description="Created via factory")

    # Verify it has a unique ID
    assert task.id is not None
    assert isinstance(task.id, str)
    assert len(task.id) > 0

    # Verify other attributes are set correctly
    assert task.title == "Factory Task"
    assert task.description == "Created via factory"
    assert task.status == TaskStatus.INCOMPLETE  # Default status
    assert task.priority == TaskPriority.MEDIUM  # Default priority

    # Create multiple tasks and verify they have unique IDs
    task1 = Task.create(title="Task 1")
    task2 = Task.create(title="Task 2")

    assert task1.id != task2.id, "Each task should have a unique ID"