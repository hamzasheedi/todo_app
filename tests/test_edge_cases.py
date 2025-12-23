"""
Tests for edge cases in the Todo CLI application.
"""
import tempfile
from pathlib import Path
from src.cli.commands import TaskManager


def test_empty_title_edge_case_127():
    """Test handling of empty title (Edge Case #127)."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        from src.storage.json_storage import JSONStorage
        task_manager.storage = JSONStorage(str(storage_file))

        # Test empty string
        try:
            task_manager.add_task("")
            assert False, "Expected ValueError for empty title"
        except ValueError as e:
            assert "cannot be empty" in str(e)

        # Test whitespace-only title
        try:
            task_manager.add_task("   ")
            assert False, "Expected ValueError for whitespace-only title"
        except ValueError as e:
            assert "cannot be empty" in str(e)

        # Test title with only spaces
        try:
            task_manager.add_task(" \t\n ")
            assert False, "Expected ValueError for whitespace-only title"
        except ValueError as e:
            assert "cannot be empty" in str(e)


def test_duplicate_task_edge_case_134():
    """Test handling of duplicate task creation (Edge Case #134)."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        from src.storage.json_storage import JSONStorage
        task_manager.storage = JSONStorage(str(storage_file))

        # Add a task
        task_manager.add_task("Test Task", description="First task")

        # Try to add the same task again (should fail)
        try:
            task_manager.add_task("Test Task", description="Duplicate task")
            assert False, "Expected ValueError for duplicate task"
        except ValueError as e:
            assert "already exists" in str(e)

        # Try to add a task with different case (should also fail)
        try:
            task_manager.add_task("test task", description="Different case task")
            assert False, "Expected ValueError for duplicate task with different case"
        except ValueError as e:
            assert "already exists" in str(e)

        # Add a different task (should work)
        task_manager.add_task("Different Task", description="This should work")