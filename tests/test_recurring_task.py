"""
Tests for the RecurringTask entity class.
"""
from datetime import datetime, timedelta
from src.core.task import Task
from src.core.recurring_task import RecurringTask, RecurrenceRule, ContinuePolicy


def test_recurring_task_creation():
    """Test basic recurring task creation."""
    # Create a base task
    base_task = Task(title="Water plants", description="Water the garden plants")

    # Create a recurring task
    recurring_task = RecurringTask(
        base_task=base_task,
        recurrence_rule=RecurrenceRule.DAILY,
        next_occurrence=(datetime.now() + timedelta(days=1)).isoformat()
    )

    assert recurring_task.base_task.title == "Water plants"
    assert recurring_task.recurrence_rule == RecurrenceRule.DAILY
    assert recurring_task.is_active is True
    assert recurring_task.continue_after_completion == ContinuePolicy.ALWAYS_CONTINUE
    assert recurring_task.id is not None


def test_recurring_task_validation():
    """Test recurring task validation rules."""
    base_task = Task(title="Test task")

    # Test that next occurrence must be in the future
    future_date = (datetime.now() + timedelta(days=1)).isoformat()
    past_date = (datetime.now() - timedelta(days=1)).isoformat()

    # This should work (future date)
    recurring_task = RecurringTask(
        base_task=base_task,
        recurrence_rule=RecurrenceRule.WEEKLY,
        next_occurrence=future_date
    )
    assert recurring_task.next_occurrence == future_date

    # Test that end date must be after next occurrence
    next_date = (datetime.now() + timedelta(days=2)).isoformat()
    end_date = (datetime.now() + timedelta(days=1)).isoformat()

    try:
        RecurringTask(
            base_task=base_task,
            recurrence_rule=RecurrenceRule.MONTHLY,
            next_occurrence=next_date,
            end_date=end_date  # end_date is before next_occurrence, should fail
        )
        assert False, "Expected ValueError for end date before next occurrence"
    except ValueError:
        pass  # Expected


def test_calculate_next_occurrence():
    """Test calculation of next occurrence."""
    base_task = Task(title="Test task")
    current_date = datetime.now()
    next_date = (current_date + timedelta(days=1)).isoformat()

    recurring_task = RecurringTask(
        base_task=base_task,
        recurrence_rule=RecurrenceRule.DAILY,
        next_occurrence=next_date
    )

    # Test daily recurrence
    expected_next = recurring_task.calculate_next_occurrence()
    assert expected_next != next_date  # Should be different date

    # Test weekly recurrence
    recurring_task.recurrence_rule = RecurrenceRule.WEEKLY
    expected_next_weekly = recurring_task.calculate_next_occurrence()
    assert expected_next_weekly != next_date

    # Test monthly recurrence
    recurring_task.recurrence_rule = RecurrenceRule.MONTHLY
    expected_next_monthly = recurring_task.calculate_next_occurrence()
    assert expected_next_monthly != next_date

    # Test yearly recurrence
    recurring_task.recurrence_rule = RecurrenceRule.YEARLY
    expected_next_yearly = recurring_task.calculate_next_occurrence()
    assert expected_next_yearly != next_date


def test_should_generate_new_task():
    """Test logic for determining if a new task should be generated."""
    base_task = Task(title="Test task")

    # Test with future next occurrence (should not generate)
    future_date = (datetime.now() + timedelta(days=1)).isoformat()
    recurring_task = RecurringTask(
        base_task=base_task,
        recurrence_rule=RecurrenceRule.DAILY,
        next_occurrence=future_date
    )

    assert recurring_task.should_generate_new_task() is False

    # Test with inactive recurring task (should not generate)
    recurring_task.is_active = False
    assert recurring_task.should_generate_new_task() is False

    # Reset to active for further tests
    recurring_task.is_active = True
    # For this test, we'll bypass the validation by directly setting the internal attribute
    # since we can't set a past date through the setter due to validation
    past_date = (datetime.now() - timedelta(days=1)).isoformat()
    recurring_task._next_occurrence = past_date
    assert recurring_task.should_generate_new_task() is True


def test_generate_task_instance():
    """Test generation of task instances."""
    from src.core.task import TaskPriority
    base_task = Task(
        title="Water plants",
        description="Water the garden plants",
        priority=TaskPriority.HIGH,
        tags=["garden", "daily"]
    )

    recurring_task = RecurringTask(
        base_task=base_task,
        recurrence_rule=RecurrenceRule.DAILY,
        next_occurrence=(datetime.now() + timedelta(days=1)).isoformat()
    )

    # Generate a task instance
    task_instance = recurring_task.generate_task_instance()

    # Verify properties are copied correctly
    assert task_instance.title == "Water plants"
    assert task_instance.description == "Water the garden plants"
    assert task_instance.priority.name.lower() == "high"
    assert "garden" in task_instance.tags
    assert "daily" in task_instance.tags

    # Verify the instance has a different ID
    assert task_instance.id != base_task.id

    # Verify the instance is incomplete (regardless of base task status)
    assert task_instance.status.name.lower() == "incomplete"


def test_update_next_occurrence():
    """Test updating the next occurrence."""
    base_task = Task(title="Test task")
    current_date = (datetime.now() + timedelta(days=1)).isoformat()

    recurring_task = RecurringTask(
        base_task=base_task,
        recurrence_rule=RecurrenceRule.DAILY,
        next_occurrence=current_date
    )

    original_next = recurring_task.next_occurrence

    # Update the next occurrence
    recurring_task.update_next_occurrence()

    # Verify it's different from the original
    assert recurring_task.next_occurrence != original_next


def test_serialization():
    """Test serialization and deserialization of RecurringTask."""
    from src.core.task import TaskPriority
    base_task = Task(
        title="Serialize test",
        description="Test serialization",
        priority=TaskPriority.MEDIUM
    )

    original_recurring_task = RecurringTask(
        base_task=base_task,
        recurrence_rule=RecurrenceRule.WEEKLY,
        next_occurrence=(datetime.now() + timedelta(days=7)).isoformat(),
        continue_after_completion=ContinuePolicy.PROMPT_USER
    )

    # Convert to dict
    recurring_task_dict = original_recurring_task.to_dict()

    # Convert back from dict
    restored_recurring_task = RecurringTask.from_dict(recurring_task_dict)

    # Verify properties are preserved
    assert restored_recurring_task.base_task.title == "Serialize test"
    assert restored_recurring_task.recurrence_rule == RecurrenceRule.WEEKLY
    assert restored_recurring_task.continue_after_completion == ContinuePolicy.PROMPT_USER
    assert restored_recurring_task.id == original_recurring_task.id


def test_equality():
    """Test equality comparison for RecurringTask."""
    base_task = Task(title="Test task")
    future_date = (datetime.now() + timedelta(days=1)).isoformat()

    recurring_task1 = RecurringTask(
        base_task=base_task,
        recurrence_rule=RecurrenceRule.DAILY,
        next_occurrence=future_date
    )

    recurring_task2 = RecurringTask(
        base_task=base_task,
        recurrence_rule=RecurrenceRule.DAILY,
        next_occurrence=future_date
    )

    # Different recurring tasks with same properties should not be equal
    assert recurring_task1 != recurring_task2

    # Same recurring task (by ID) should be equal - this is tested by assigning same ID
    recurring_task2._id = recurring_task1.id
    assert recurring_task1 == recurring_task2


def test_string_representation():
    """Test string representations."""
    base_task = Task(title="Weekly meeting")
    recurring_task = RecurringTask(
        base_task=base_task,
        recurrence_rule=RecurrenceRule.WEEKLY,
        next_occurrence=(datetime.now() + timedelta(days=7)).isoformat()
    )

    str_repr = str(recurring_task)
    assert "Weekly meeting" in str_repr
    assert "WEEKLY" in str_repr or "weekly" in str_repr.lower()

    repr_repr = repr(recurring_task)
    assert "Weekly meeting" in repr_repr
    assert recurring_task.id in repr_repr