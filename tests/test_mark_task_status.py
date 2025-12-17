"""
Tests for mark task status functionality (complete/incomplete).
"""
import tempfile
from pathlib import Path
from src.core.task import TaskStatus
from src.cli.commands import TaskManager


def test_mark_task_status():
    """Test mark task as complete/incomplete functionality."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        from src.storage.json_storage import JSONStorage
        task_manager.storage = JSONStorage(str(storage_file))

        # Add a task
        task = task_manager.add_task("Test Task", description="Task for status testing")

        # Verify initial status is incomplete
        assert task.status == TaskStatus.INCOMPLETE

        # Mark as complete
        result = task_manager.mark_task_status(task.id, "complete")
        assert result is True

        # Verify status is now complete
        updated_task = task_manager.get_task(task.id)
        assert updated_task.status == TaskStatus.COMPLETE

        # Mark as incomplete
        result = task_manager.mark_task_status(updated_task.id, "incomplete")
        assert result is True

        # Verify status is now incomplete
        final_task = task_manager.get_task(task.id)
        assert final_task.status == TaskStatus.INCOMPLETE

        # Try to mark with invalid status (should fail)
        result = task_manager.mark_task_status(task.id, "invalid")
        assert result is False, "Should return False for invalid status"

        # Try to mark non-existent task (should fail)
        result = task_manager.mark_task_status("non-existent-id", "complete")
        assert result is False, "Should return False for non-existent task"