"""
Tests for delete task functionality with error feedback.
"""
import tempfile
from pathlib import Path
from src.cli.commands import TaskManager


def test_delete_task_with_feedback():
    """Test delete task functionality with error feedback (FR-016)."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        from src.storage.json_storage import JSONStorage
        task_manager.storage = JSONStorage(str(storage_file))

        # Add some tasks
        task1 = task_manager.add_task("Task 1", description="First task")
        task2 = task_manager.add_task("Task 2", description="Second task")

        # Try to delete a non-existent task
        result = task_manager.delete_task_with_feedback("non-existent-id")
        assert result is False, "Should return False when task doesn't exist"

        # Verify the existing tasks are still there
        remaining_tasks = task_manager.storage.load_tasks()
        assert len(remaining_tasks) == 2, "Should still have 2 tasks after failed deletion"

        # Delete an existing task
        result = task_manager.delete_task_with_feedback(task1.id)
        assert result is True, "Should return True when task is successfully deleted"

        # Verify only one task remains
        remaining_tasks = task_manager.storage.load_tasks()
        assert len(remaining_tasks) == 1, "Should have 1 task after successful deletion"
        assert remaining_tasks[0].id == task2.id, "Should be the second task that remains"