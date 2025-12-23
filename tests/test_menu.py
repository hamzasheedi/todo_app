"""
Tests for the CLI menu system.
"""
import tempfile
from pathlib import Path
from src.cli.commands import TaskManager
from src.cli.menu import view_all_tasks, add_new_task, delete_existing_task


def test_menu_functions():
    """Test basic menu functions work correctly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        from src.storage.json_storage import JSONStorage
        task_manager.storage = JSONStorage(str(storage_file))

        # Test adding a task (simulating menu add function)
        # We'll call the underlying function directly since the menu functions
        # require user input
        task = task_manager.add_task("Test Task", description="Test description")
        assert task.title == "Test Task"

        # Test viewing tasks
        tasks = task_manager.view_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Test Task"

        # Test deleting a task
        result = task_manager.delete_task_with_feedback(task.id)
        assert result is True

        # Verify task is gone
        tasks = task_manager.view_tasks()
        assert len(tasks) == 0

        print("All menu function tests passed!")