"""
Tests for the CLI command handlers.
"""
import tempfile
from pathlib import Path
from src.core.task import Task, TaskStatus, TaskPriority
from src.cli.commands import add_task, view_tasks, update_task, delete_task, mark_task_status, get_task, TaskManager


def test_add_task_basic():
    """Test adding a basic task."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        # Override the storage to use our temporary file
        from src.storage.json_storage import JSONStorage
        task_manager.storage = JSONStorage(str(storage_file))

        # Add a task
        task = task_manager.add_task("Test Task")

        # Verify task was created
        assert task.title == "Test Task"
        assert task.status == TaskStatus.INCOMPLETE
        assert task.priority == TaskPriority.MEDIUM  # Default priority
        assert task.id is not None


def test_add_task_with_details():
    """Test adding a task with all details."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        from src.storage.json_storage import JSONStorage
        task_manager.storage = JSONStorage(str(storage_file))

        # Add a task with all details
        task = task_manager.add_task(
            title="Complete Project",
            description="Finish the todo app project",
            priority="high",
            tags=["work", "urgent"],
            due_date="2025-12-31T10:00:00"
        )

        # Verify all details were set correctly
        assert task.title == "Complete Project"
        assert task.description == "Finish the todo app project"
        assert task.priority == TaskPriority.HIGH
        assert "work" in task.tags
        assert "urgent" in task.tags
        assert task.due_date == "2025-12-31T10:00:00"


def test_view_tasks():
    """Test viewing tasks."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        from src.storage.json_storage import JSONStorage
        task_manager = TaskManager()
        task_manager.storage = JSONStorage(str(storage_file))

        # Add some tasks
        task1 = task_manager.add_task("Task 1", priority="high")
        task2 = task_manager.add_task("Task 2", priority="low")

        # Mark one as complete
        task_manager.mark_task_status(task2.id, "complete")

        # View all tasks
        all_tasks = task_manager.view_tasks()
        assert len(all_tasks) == 2

        # View only incomplete tasks
        incomplete_tasks = task_manager.view_tasks(status="incomplete")
        assert len(incomplete_tasks) == 1
        assert incomplete_tasks[0].id == task1.id

        # View only complete tasks
        complete_tasks = task_manager.view_tasks(status="complete")
        assert len(complete_tasks) == 1
        assert complete_tasks[0].id == task2.id

        # View by priority
        high_priority_tasks = task_manager.view_tasks(priority="high")
        assert len(high_priority_tasks) == 1
        assert high_priority_tasks[0].id == task1.id


def test_update_task():
    """Test updating a task."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        from src.storage.json_storage import JSONStorage
        task_manager.storage = JSONStorage(str(storage_file))

        # Add a task
        original_task = task_manager.add_task("Original Title", description="Original Description")

        # Update the task
        result = task_manager.update_task(
            task_id=original_task.id,
            title="Updated Title",
            description="Updated Description",
            priority="high"
        )

        assert result is True  # Update successful

        # Get the updated task
        updated_task = task_manager.get_task(original_task.id)
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        assert updated_task.priority == TaskPriority.HIGH


def test_delete_task():
    """Test deleting a task."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        from src.storage.json_storage import JSONStorage
        task_manager.storage = JSONStorage(str(storage_file))

        # Add a task
        task = task_manager.add_task("Task to Delete")

        # Verify task exists
        assert task_manager.get_task(task.id) is not None

        # Delete the task
        result = task_manager.delete_task(task.id)
        assert result is True

        # Verify task no longer exists
        assert task_manager.get_task(task.id) is None


def test_mark_task_status():
    """Test marking task status."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        from src.storage.json_storage import JSONStorage
        task_manager.storage = JSONStorage(str(storage_file))

        # Add a task
        task = task_manager.add_task("Status Test Task")

        # Verify initial status is incomplete
        assert task.status == TaskStatus.INCOMPLETE

        # Mark as complete
        result = task_manager.mark_task_status(task.id, "complete")
        assert result is True

        # Verify status is now complete
        updated_task = task_manager.get_task(task.id)
        assert updated_task.status == TaskStatus.COMPLETE

        # Mark as incomplete again
        result = task_manager.mark_task_status(updated_task.id, "incomplete")
        assert result is True

        # Verify status is now incomplete
        final_task = task_manager.get_task(task.id)
        assert final_task.status == TaskStatus.INCOMPLETE


def test_get_task():
    """Test getting a specific task by ID."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        from src.storage.json_storage import JSONStorage
        task_manager.storage = JSONStorage(str(storage_file))

        # Add a task
        original_task = task_manager.add_task("Get Test Task", description="Test getting task by ID")

        # Get the task by ID
        retrieved_task = task_manager.get_task(original_task.id)
        assert retrieved_task is not None
        assert retrieved_task.id == original_task.id
        assert retrieved_task.title == "Get Test Task"
        assert retrieved_task.description == "Test getting task by ID"

        # Try to get a non-existent task
        non_existent_task = task_manager.get_task("nonexistent-id")
        assert non_existent_task is None


def test_task_validation_in_commands():
    """Test that validation rules are enforced in command handlers."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        from src.storage.json_storage import JSONStorage
        task_manager.storage = JSONStorage(str(storage_file))

        # Try to add a task with empty title (should fail)
        try:
            task_manager.add_task("")
            assert False, "Expected ValueError for empty title"
        except ValueError:
            pass  # Expected

        # Try to add a task with invalid priority (should fail)
        try:
            task_manager.add_task("Test Task", priority="invalid")
            assert False, "Expected ValueError for invalid priority"
        except ValueError:
            pass  # Expected

        # Try to update a task with invalid status (should fail)
        task = task_manager.add_task("Test Task")
        try:
            task_manager.update_task(task.id, status="invalid")
            assert False, "Expected ValueError for invalid status"
        except ValueError:
            pass  # Expected

        # Try to mark task status with invalid status (should return False)
        result = task_manager.mark_task_status(task.id, "invalid")
        assert result is False, "Should return False for invalid status"