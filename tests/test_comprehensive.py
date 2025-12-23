"""
Comprehensive test suite for the entire Todo CLI application.

This test verifies that all components work together correctly.
"""
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from src.core.task import Task, TaskStatus, TaskPriority
from src.cli.commands import TaskManager
from src.storage.json_storage import JSONStorage


def test_comprehensive_workflow():
    """Test the complete workflow of the todo application."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "comprehensive_test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        task_manager.storage = JSONStorage(str(storage_file))

        # 1. Add several tasks with different properties
        task1 = task_manager.add_task(
            title="Complete project proposal",
            description="Write and submit the project proposal",
            priority="high",
            tags=["work", "important"],
            due_date=(datetime.now() + timedelta(days=7)).isoformat()
        )

        task2 = task_manager.add_task(
            title="Buy groceries",
            description="Buy food for the week",
            priority="medium",
            tags=["personal"],
            due_date=(datetime.now() + timedelta(days=2)).isoformat()
        )

        task3 = task_manager.add_task(
            title="Schedule team meeting",
            description="Schedule team sync for next week",
            priority="medium",
            tags=["work"],
            due_date=None
        )

        # Verify tasks were added correctly
        all_tasks = task_manager.view_tasks()
        assert len(all_tasks) == 3

        # 2. View tasks with different filters
        high_priority_tasks = task_manager.view_tasks(priority="high")
        assert len(high_priority_tasks) == 1
        assert high_priority_tasks[0].id == task1.id

        work_tasks = task_manager.view_tasks(tag="work")
        assert len(work_tasks) == 2
        work_task_ids = {task.id for task in work_tasks}
        assert task1.id in work_task_ids
        assert task3.id in work_task_ids

        # 3. Update a task
        result = task_manager.update_task(
            task_id=task2.id,
            title="Buy groceries and household items",
            description="Buy food and cleaning supplies for the week",
            priority="high"
        )
        assert result is True

        # Verify the update
        updated_task2 = task_manager.get_task(task2.id)
        assert updated_task2.title == "Buy groceries and household items"
        assert updated_task2.priority == TaskPriority.HIGH

        # 4. Mark a task as complete
        result = task_manager.mark_task_status(task1.id, "complete")
        assert result is True

        # Verify the status change
        completed_task = task_manager.get_task(task1.id)
        assert completed_task.status == TaskStatus.COMPLETE

        # 5. View tasks by status
        incomplete_tasks = task_manager.view_tasks(status="incomplete")
        assert len(incomplete_tasks) == 2  # task2 and task3

        complete_tasks = task_manager.view_tasks(status="complete")
        assert len(complete_tasks) == 1
        assert complete_tasks[0].id == task1.id

        # 6. Add more tasks to test concurrent reminders validation
        future_time = (datetime.now() + timedelta(hours=1)).isoformat()

        # Add multiple tasks with the same due date to test concurrent validation
        reminder_tasks = []
        for i in range(5):
            task = task_manager.add_task(
                title=f"Reminder task {i+1}",
                due_date=future_time  # Using due_date instead of reminder_time
            )
            # Create reminder objects separately for testing
            from src.core.reminder import Reminder
            reminder = Reminder(
                task_id=task.id,
                reminder_time=future_time
            )
            reminder_tasks.append(reminder)

        # Test that we can have up to 5 concurrent reminders at the same time
        from src.utils.validators import validate_concurrent_reminders
        result = validate_concurrent_reminders(reminder_tasks, future_time, max_concurrent=5)
        assert result is True  # 5 reminders with max of 5 should be OK

        # Add one more to exceed the limit
        sixth_reminder = Reminder(
            task_id="test_task_6",
            reminder_time=future_time
        )
        all_reminders = reminder_tasks + [sixth_reminder]
        result = validate_concurrent_reminders(all_reminders, future_time, max_concurrent=5)
        assert result is False  # 6 reminders with max of 5 should fail

        # 7. Delete a task
        result = task_manager.delete_task(task3.id)
        assert result is True

        # Verify deletion
        remaining_tasks = task_manager.view_tasks()
        # Original 3 tasks + 5 reminder tasks created in loop = 8 total
        # After deleting 1 task: 8 - 1 = 7 remaining
        assert len(remaining_tasks) == 7

        # 8. Test date/time validation edge cases
        from src.utils.validators import validate_iso_datetime, validate_datetime_with_grace_period

        # Valid datetime formats
        assert validate_iso_datetime("2025-12-31T10:00:00") is True
        assert validate_iso_datetime("2025-12-31T10:00:00Z") is True
        assert validate_iso_datetime("2025-12-31T10:00:00+00:00") is True

        # Invalid formats (date only or wrong format)
        assert validate_iso_datetime("2025-12-31") is False  # Date only
        assert validate_iso_datetime("2025-13-31T10:00:00") is False  # Invalid month
        assert validate_iso_datetime("invalid-date") is False  # Not a date at all

        # Test datetime with grace period
        future_time = (datetime.now() + timedelta(minutes=10)).isoformat()
        assert validate_datetime_with_grace_period(future_time) is True

        # Test edge case validation
        from src.utils.validators import validate_future_datetime
        past_time = (datetime.now() - timedelta(minutes=10)).isoformat()
        assert validate_future_datetime(past_time) is False  # Past should be invalid
        assert validate_future_datetime(future_time) is True  # Future should be valid

        print("All comprehensive workflow tests passed!")


def test_error_handling():
    """Test error handling and edge cases."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "error_test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        task_manager.storage = JSONStorage(str(storage_file))

        # Test adding task with empty title (should fail)
        try:
            task_manager.add_task("")
            assert False, "Expected ValueError for empty title"
        except ValueError:
            pass  # Expected

        # Test updating non-existent task
        result = task_manager.update_task("non-existent-id", title="New Title")
        assert result is False

        # Test getting non-existent task
        task = task_manager.get_task("non-existent-id")
        assert task is None

        # Test deleting non-existent task
        result = task_manager.delete_task("non-existent-id")
        assert result is False

        # Test marking status of non-existent task
        result = task_manager.mark_task_status("non-existent-id", "complete")
        assert result is False

        # Test with invalid status
        task = task_manager.add_task("Test Task")
        result = task_manager.mark_task_status(task.id, "invalid-status")
        assert result is False

        print("All error handling tests passed!")


def test_validator_functions():
    """Test all validator functions."""
    from src.utils.validators import (
        validate_iso_datetime,
        parse_datetime,
        validate_datetime_in_range,
        validate_timezone_format,
        normalize_datetime_string,
        validate_future_datetime,
        validate_datetime_with_grace_period,
        validate_concurrent_reminders
    )
    from datetime import datetime, timedelta

    # Test ISO datetime validation
    assert validate_iso_datetime("2025-12-31T10:00:00") is True
    assert validate_iso_datetime("2025-12-31T10:00:00Z") is True
    assert validate_iso_datetime("2025-12-31T10:00:00+00:00") is True
    assert validate_iso_datetime("2025-12-31") is False  # Date only
    assert validate_iso_datetime("invalid") is False

    # Test datetime parsing
    dt = parse_datetime("2025-12-31T10:00:00")
    assert dt is not None
    assert dt.year == 2025
    assert parse_datetime("invalid") is None

    # Test datetime range validation
    min_date = datetime(2025, 1, 1)
    max_date = datetime(2025, 12, 31)
    assert validate_datetime_in_range("2025-06-01T10:00:00", min_date, max_date) is True
    assert validate_datetime_in_range("2024-06-01T10:00:00", min_date, max_date) is False

    # Test timezone format
    assert validate_timezone_format("2025-12-31T10:00:00Z") is True
    assert validate_timezone_format("2025-12-31T10:00:00+00:00") is True
    assert validate_timezone_format("2025-12-31T10:00:00") is True

    # Test datetime normalization
    normalized = normalize_datetime_string("2025-12-31T10:00:00")
    assert "2025-12-31T10:00:00" in normalized

    # Test future datetime validation
    future_time = (datetime.now() + timedelta(hours=1)).isoformat()
    past_time = (datetime.now() - timedelta(hours=1)).isoformat()
    assert validate_future_datetime(future_time) is True
    assert validate_future_datetime(past_time) is False

    # Test datetime with grace period
    just_past = (datetime.now() - timedelta(minutes=3)).isoformat()
    # This should be valid with default 5-minute grace period
    assert validate_datetime_with_grace_period(just_past) is True

    further_past = (datetime.now() - timedelta(minutes=10)).isoformat()
    # This should be invalid with default 5-minute grace period
    assert validate_datetime_with_grace_period(further_past) is False

    # Test concurrent reminders validation
    from src.core.reminder import Reminder
    test_reminders = []
    test_time = (datetime.now() + timedelta(hours=1)).isoformat()

    for i in range(3):
        reminder = Reminder(
            task_id=f"task{i}",
            reminder_time=test_time
        )
        test_reminders.append(reminder)

    # Should allow 3 reminders with max_concurrent=5
    assert validate_concurrent_reminders(test_reminders, test_time, max_concurrent=5) is True

    # Should reject 6 reminders with max_concurrent=5
    for i in range(3, 6):
        reminder = Reminder(
            task_id=f"task{i}",
            reminder_time=test_time
        )
        test_reminders.append(reminder)

    assert validate_concurrent_reminders(test_reminders, test_time, max_concurrent=5) is False
    # But should allow with max_concurrent=6
    assert validate_concurrent_reminders(test_reminders, test_time, max_concurrent=6) is True

    print("All validator function tests passed!")


if __name__ == "__main__":
    test_comprehensive_workflow()
    test_error_handling()
    test_validator_functions()
    print("🎉 All comprehensive tests passed!")