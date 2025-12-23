"""
Tests for sort functionality.
"""
import tempfile
from pathlib import Path
from src.cli.commands import TaskManager
from src.core.task import TaskPriority


def test_sort_functionality():
    """Test sort functionality for tasks."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        from src.storage.json_storage import JSONStorage
        task_manager.storage = JSONStorage(str(storage_file))

        # Add tasks with different priorities, due dates, and titles
        task_low = task_manager.add_task("Low priority task", priority="low")
        task_high1 = task_manager.add_task("High priority task 1", priority="high")
        task_medium = task_manager.add_task("Medium priority task", priority="medium")
        task_high2 = task_manager.add_task("High priority task 2", priority="high",
                                          due_date="2025-01-01T10:00:00")
        task_no_priority = task_manager.add_task("No priority task")  # Will have default medium

        # Test sorting by priority (high -> medium -> low)
        all_tasks = [task_low, task_high1, task_medium, task_high2, task_no_priority]
        sorted_tasks = task_manager.sort_tasks(all_tasks, 'priority')

        # Check that high priority tasks come first
        high_tasks = [task for task in sorted_tasks if task.priority == TaskPriority.HIGH]
        medium_tasks = [task for task in sorted_tasks if task.priority == TaskPriority.MEDIUM]
        low_tasks = [task for task in sorted_tasks if task.priority == TaskPriority.LOW]

        # Verify the order: high priority tasks first, then medium, then low
        assert sorted_tasks[0].priority == TaskPriority.HIGH
        assert sorted_tasks[1].priority == TaskPriority.HIGH
        assert sorted_tasks[2].priority == TaskPriority.MEDIUM
        assert sorted_tasks[3].priority == TaskPriority.MEDIUM
        assert sorted_tasks[4].priority == TaskPriority.LOW

        # Test sorting by alphabetical order
        sorted_alpha = task_manager.sort_tasks(all_tasks, 'alphabetical')
        titles = [task.title for task in sorted_alpha]
        expected_order = sorted(titles, key=str.lower)
        assert titles == expected_order, f"Expected {expected_order}, got {titles}"

        # Test sorting by due date
        sorted_due_date = task_manager.sort_tasks(all_tasks, 'due_date')
        # Tasks with due dates should come first, then those without
        has_due_date = [task for task in sorted_due_date if task.due_date is not None]
        no_due_date = [task for task in sorted_due_date if task.due_date is None]
        # The task with due date should appear first
        assert len(has_due_date) == 1
        assert has_due_date[0].due_date == "2025-01-01T10:00:00"

        # Test reverse sorting by priority
        sorted_reverse = task_manager.sort_tasks(all_tasks, 'priority', reverse=True)
        # Now low priority should come first
        assert sorted_reverse[0].priority == TaskPriority.LOW
        assert sorted_reverse[-1].priority == TaskPriority.HIGH

        # Test get_sorted_tasks with filters
        high_priority_tasks = task_manager.get_sorted_tasks('priority', {'priority': 'high'})
        assert len(high_priority_tasks) == 2  # task_high1 and task_high2
        for task in high_priority_tasks:
            assert task.priority == TaskPriority.HIGH

        # Test with no filters but with sorting
        all_sorted_by_priority = task_manager.get_sorted_tasks('priority')
        original_tasks = task_manager.storage.load_tasks()
        assert len(all_sorted_by_priority) == len(original_tasks)

        print("All sort functionality tests passed!")