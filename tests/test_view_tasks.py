"""
Tests for the view tasks functionality.
"""
import tempfile
from pathlib import Path
from src.cli.commands import TaskManager


def test_empty_task_list_edge_case_135():
    """Test handling of empty task list (Edge Case #135)."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        from src.storage.json_storage import JSONStorage
        task_manager.storage = JSONStorage(str(storage_file))

        # Get all tasks when list is empty
        tasks = task_manager.view_tasks()
        assert len(tasks) == 0, "Should return empty list when no tasks exist"

        # Get tasks with filters when list is empty
        filtered_tasks = task_manager.view_tasks(status="incomplete")
        assert len(filtered_tasks) == 0, "Should return empty list when no tasks match filter"

        filtered_tasks = task_manager.view_tasks(priority="high")
        assert len(filtered_tasks) == 0, "Should return empty list when no tasks match priority filter"

        filtered_tasks = task_manager.view_tasks(tag="work")
        assert len(filtered_tasks) == 0, "Should return empty list when no tasks match tag filter"

        # Verify that the storage file exists but is empty list
        all_tasks = task_manager.storage.load_tasks()
        assert len(all_tasks) == 0, "Storage should contain empty list"