"""
Tests for the JSON storage manager.
"""
import json
import tempfile
from pathlib import Path
from src.core.task import Task, TaskStatus, TaskPriority
from src.storage.json_storage import JSONStorage


def test_json_storage_initialization():
    """Test JSON storage initialization."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"
        storage = JSONStorage(str(storage_file))

        assert storage.file_path == storage_file


def test_save_and_load_empty_tasks():
    """Test saving and loading an empty list of tasks."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"
        storage = JSONStorage(str(storage_file))

        # Save empty list
        storage.save_tasks([])

        # Load and verify
        tasks = storage.load_tasks()
        assert len(tasks) == 0


def test_save_and_load_tasks():
    """Test saving and loading tasks."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"
        storage = JSONStorage(str(storage_file))

        # Create test tasks
        task1 = Task.create(title="Task 1", description="First task")
        task2 = Task.create(
            title="Task 2",
            description="Second task",
            priority=TaskPriority.HIGH,
            tags=["work", "urgent"],
            due_date="2025-12-31T10:00:00"
        )

        tasks = [task1, task2]

        # Save tasks
        storage.save_tasks(tasks)

        # Load tasks
        loaded_tasks = storage.load_tasks()

        # Verify tasks were loaded correctly
        assert len(loaded_tasks) == 2
        assert loaded_tasks[0].title == "Task 1"
        assert loaded_tasks[1].title == "Task 2"
        assert loaded_tasks[1].priority == TaskPriority.HIGH
        assert "work" in loaded_tasks[1].tags
        assert loaded_tasks[1].due_date == "2025-12-31T10:00:00"

        # Verify IDs are preserved
        assert loaded_tasks[0].id == task1.id
        assert loaded_tasks[1].id == task2.id


def test_add_task():
    """Test adding a single task."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"
        storage = JSONStorage(str(storage_file))

        # Start with empty storage
        assert len(storage.load_tasks()) == 0

        # Add a task
        task = Task.create(title="New Task")
        storage.add_task(task)

        # Verify task was added
        tasks = storage.load_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "New Task"


def test_update_task():
    """Test updating a task."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"
        storage = JSONStorage(str(storage_file))

        # Add a task
        original_task = Task.create(title="Original Title")
        storage.add_task(original_task)

        # Create updated task
        updated_task = Task(
            id=original_task.id,
            title="Updated Title",
            description="Updated Description",
            status=TaskStatus.COMPLETE
        )

        # Update the task
        result = storage.update_task(original_task.id, updated_task)
        assert result is True

        # Verify the task was updated
        tasks = storage.load_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Updated Title"
        assert tasks[0].description == "Updated Description"
        assert tasks[0].status == TaskStatus.COMPLETE


def test_update_nonexistent_task():
    """Test updating a non-existent task."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"
        storage = JSONStorage(str(storage_file))

        # Try to update a non-existent task
        fake_task = Task.create(title="Fake Task")
        result = storage.update_task("nonexistent-id", fake_task)
        assert result is False


def test_delete_task():
    """Test deleting a task."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"
        storage = JSONStorage(str(storage_file))

        # Add multiple tasks
        task1 = Task.create(title="Task 1")
        task2 = Task.create(title="Task 2")
        storage.add_task(task1)
        storage.add_task(task2)

        # Verify both tasks exist
        tasks = storage.load_tasks()
        assert len(tasks) == 2

        # Delete one task
        result = storage.delete_task(task1.id)
        assert result is True

        # Verify only one task remains
        tasks = storage.load_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == task2.id


def test_delete_nonexistent_task():
    """Test deleting a non-existent task."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"
        storage = JSONStorage(str(storage_file))

        # Try to delete a non-existent task
        result = storage.delete_task("nonexistent-id")
        assert result is False


def test_task_exists():
    """Test checking if a task exists."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"
        storage = JSONStorage(str(storage_file))

        # Add a task
        task = Task.create(title="Test Task")
        storage.add_task(task)

        # Check that it exists
        assert storage.task_exists(task.id) is True

        # Check that a non-existent task doesn't exist
        assert storage.task_exists("nonexistent-id") is False


def test_clear_all_tasks():
    """Test clearing all tasks."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"
        storage = JSONStorage(str(storage_file))

        # Add some tasks
        task1 = Task.create(title="Task 1")
        task2 = Task.create(title="Task 2")
        storage.add_task(task1)
        storage.add_task(task2)

        # Verify tasks exist
        assert len(storage.load_tasks()) == 2

        # Clear all tasks
        storage.clear_all_tasks()

        # Verify no tasks remain
        assert len(storage.load_tasks()) == 0


def test_get_task():
    """Test getting a specific task by ID."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"
        storage = JSONStorage(str(storage_file))

        # Add a task
        original_task = Task.create(title="Test Task", description="Test Description")
        storage.add_task(original_task)

        # Retrieve the task
        retrieved_task = storage.get_task(original_task.id)
        assert retrieved_task is not None
        assert retrieved_task.title == "Test Task"
        assert retrieved_task.description == "Test Description"
        assert retrieved_task.id == original_task.id

        # Try to get a non-existent task
        non_existent_task = storage.get_task("nonexistent-id")
        assert non_existent_task is None


def test_file_not_found():
    """Test behavior when storage file doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "nonexistent.json"
        storage = JSONStorage(str(storage_file))

        # Should return empty list when file doesn't exist
        tasks = storage.load_tasks()
        assert len(tasks) == 0


def test_invalid_json_file():
    """Test behavior with invalid JSON file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "invalid.json"

        # Write invalid JSON to the file
        with open(storage_file, 'w') as f:
            f.write("this is not valid json")

        storage = JSONStorage(str(storage_file))

        # Should raise ValueError for invalid JSON
        try:
            storage.load_tasks()
            assert False, "Expected ValueError for invalid JSON"
        except ValueError:
            pass  # Expected


def test_invalid_task_data():
    """Test behavior with invalid task data in JSON file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "invalid_tasks.json"

        # Write JSON with invalid task data
        invalid_data = [{"invalid": "data"}, "not a task object"]
        with open(storage_file, 'w') as f:
            json.dump(invalid_data, f)

        storage = JSONStorage(str(storage_file))

        # Should raise ValueError for invalid task data
        try:
            storage.load_tasks()
            assert False, "Expected ValueError for invalid task data"
        except ValueError:
            pass  # Expected