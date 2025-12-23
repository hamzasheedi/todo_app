"""
Tests for filter functionality.
"""
import tempfile
from pathlib import Path
from src.cli.commands import TaskManager


def test_filter_functionality():
    """Test filter functionality for tasks."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        from src.storage.json_storage import JSONStorage
        task_manager.storage = JSONStorage(str(storage_file))

        # Add some tasks with different attributes
        task1 = task_manager.add_task("High priority task", priority="high", tags=["work", "urgent"])
        task_manager.mark_task_status(task1.id, "complete")  # Mark as complete

        task2 = task_manager.add_task("Medium priority task", priority="medium", tags=["personal"])
        task_manager.mark_task_status(task2.id, "incomplete")  # Keep as incomplete

        task3 = task_manager.add_task("Low priority task", priority="low", tags=["work"])
        task_manager.mark_task_status(task3.id, "incomplete")  # Keep as incomplete

        task4 = task_manager.add_task("Another urgent task", priority="high", tags=["work", "urgent"],
                                      due_date="2025-12-31T10:00:00")

        # Test filtering by status
        completed_tasks = task_manager.filter_tasks({"status": "complete"})
        assert len(completed_tasks) == 1
        assert completed_tasks[0].id == task1.id

        incomplete_tasks = task_manager.filter_tasks({"status": "incomplete"})
        assert len(incomplete_tasks) == 3

        # Test filtering by priority
        high_priority_tasks = task_manager.filter_tasks({"priority": "high"})
        assert len(high_priority_tasks) == 2  # task1 and task4

        low_priority_tasks = task_manager.filter_tasks({"priority": "low"})
        assert len(low_priority_tasks) == 1
        assert low_priority_tasks[0].id == task3.id

        # Test filtering by tags
        work_tasks = task_manager.filter_tasks({"tags": ["work"]})
        assert len(work_tasks) == 3  # task1, task3, and task4

        urgent_tasks = task_manager.filter_tasks({"tags": ["urgent"]})
        assert len(urgent_tasks) == 2  # task1 and task4

        # Test filtering by multiple tags (AND operation)
        work_and_urgent_tasks = task_manager.filter_tasks({"tags": ["work", "urgent"]})
        assert len(work_and_urgent_tasks) == 2  # task1 and task4

        # Test filtering by due date
        due_tasks = task_manager.filter_tasks({"due_date": "2025-12-31"})
        assert len(due_tasks) == 1
        assert due_tasks[0].id == task4.id

        # Test combining filters
        completed_high_tasks = task_manager.filter_tasks({"status": "complete", "priority": "high"})
        assert len(completed_high_tasks) == 1
        assert completed_high_tasks[0].id == task1.id

        incomplete_work_tasks = task_manager.filter_tasks({"status": "incomplete", "tags": ["work"]})
        assert len(incomplete_work_tasks) == 2  # task3 and task4

        # Test with no filters (should return all tasks)
        all_tasks = task_manager.filter_tasks()
        assert len(all_tasks) == 4

        # Test with empty filters dict (should return all tasks)
        all_tasks_empty_filter = task_manager.filter_tasks({})
        assert len(all_tasks_empty_filter) == 4

        print("All filter functionality tests passed!")