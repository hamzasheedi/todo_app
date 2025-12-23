"""
Tests for update task validation and edge cases.
"""
import tempfile
from pathlib import Path
from src.cli.commands import TaskManager


def test_invalid_task_id_edge_case_129():
    """Test handling of invalid task ID during update (Edge Case #129)."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        from src.storage.json_storage import JSONStorage
        task_manager.storage = JSONStorage(str(storage_file))

        # Try to update a task with a non-existent ID
        result = task_manager.update_task("non-existent-id", title="New Title")
        assert result is False, "Should return False when task ID doesn't exist"

        # Add a valid task
        task = task_manager.add_task("Valid Task", description="Original description")

        # Try to update with the correct ID (should work)
        result = task_manager.update_task(task.id, description="Updated description")
        assert result is True, "Should return True when updating valid task"

        # Verify the update worked
        updated_task = task_manager.get_task(task.id)
        assert updated_task.description == "Updated description"

        # Try to update with an invalid ID again
        result = task_manager.update_task("another-invalid-id", title="Another Title")
        assert result is False, "Should return False when task ID doesn't exist"