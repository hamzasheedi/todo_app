"""
Tests for the RecurringTaskManager class.
"""
from datetime import datetime, timedelta
from src.core.task import Task, TaskPriority
from src.core.recurring_task import RecurringTask, RecurringTaskManager, RecurrenceRule, ContinuePolicy


def test_recurring_task_manager():
    """Test the RecurringTaskManager functionality."""
    # Create a manager
    manager = RecurringTaskManager()

    # Create a base task
    base_task = Task(
        title="Water plants",
        description="Water the garden plants",
        priority=TaskPriority.MEDIUM
    )

    # Create a recurring task with a future next occurrence
    future_date = (datetime.now() + timedelta(minutes=1)).isoformat()
    recurring_task = RecurringTask(
        base_task=base_task,
        recurrence_rule=RecurrenceRule.DAILY,
        next_occurrence=future_date
    )

    # Add the recurring task to the manager
    manager.add_recurring_task(recurring_task)

    # Verify it was added
    assert len(manager.recurring_tasks) == 1
    assert manager.get_recurring_task(recurring_task.id) == recurring_task

    # Initially, no tasks should be generated since next occurrence is in the future
    new_tasks = manager.process_recurring_tasks()
    assert len(new_tasks) == 0

    # Now, let's simulate that the time has passed by directly modifying the internal state
    # This simulates what would happen in a real application after some time passes
    past_date = (datetime.now() - timedelta(minutes=2)).isoformat()
    recurring_task._next_occurrence = past_date  # Bypass validation for testing

    # Now process recurring tasks - this should generate a new task
    new_tasks = manager.process_recurring_tasks()
    assert len(new_tasks) == 1
    assert new_tasks[0].title == "Water plants"
    assert new_tasks[0].status.name.lower() == "incomplete"

    # Verify the recurring task's next occurrence was updated
    # After processing, the next occurrence should be different (updated)
    assert recurring_task.next_occurrence != past_date


def test_get_tasks_to_generate():
    """Test getting recurring tasks that should generate new instances."""
    manager = RecurringTaskManager()

    base_task = Task(title="Test task", priority=TaskPriority.MEDIUM)

    # Create recurring tasks with future dates
    future_date1 = (datetime.now() + timedelta(days=1)).isoformat()
    recurring_task_future = RecurringTask(
        base_task=base_task,
        recurrence_rule=RecurrenceRule.DAILY,
        next_occurrence=future_date1
    )

    future_date2 = (datetime.now() + timedelta(minutes=30)).isoformat()
    recurring_task_current = RecurringTask(
        base_task=base_task,
        recurrence_rule=RecurrenceRule.DAILY,
        next_occurrence=future_date2
    )

    manager.add_recurring_task(recurring_task_future)
    manager.add_recurring_task(recurring_task_current)

    # Initially, no tasks should be ready to generate since dates are in the future
    tasks_to_generate = manager.get_tasks_to_generate()
    assert len(tasks_to_generate) == 0

    # Now simulate that time has passed for one task
    past_date = (datetime.now() - timedelta(minutes=1)).isoformat()
    recurring_task_current._next_occurrence = past_date  # Bypass validation for testing

    # Now there should be one task ready to generate
    tasks_to_generate = manager.get_tasks_to_generate()
    assert len(tasks_to_generate) == 1
    assert tasks_to_generate[0].id == recurring_task_current.id


def test_enable_disable_recurring_task():
    """Test enabling and disabling recurring tasks."""
    manager = RecurringTaskManager()

    base_task = Task(title="Test task", priority=TaskPriority.MEDIUM)
    future_date = (datetime.now() + timedelta(days=1)).isoformat()
    recurring_task = RecurringTask(
        base_task=base_task,
        recurrence_rule=RecurrenceRule.DAILY,
        next_occurrence=future_date
    )

    manager.add_recurring_task(recurring_task)

    # Verify it's active
    assert recurring_task.is_active is True

    # Disable it
    result = manager.disable_recurring_task(recurring_task.id)
    assert result is True
    assert recurring_task.is_active is False

    # Try to disable a non-existent task
    result = manager.disable_recurring_task("non-existent")
    assert result is False

    # Enable it
    result = manager.enable_recurring_task(recurring_task.id)
    assert result is True
    assert recurring_task.is_active is True

    # Try to enable a non-existent task
    result = manager.enable_recurring_task("non-existent")
    assert result is False


def test_remove_recurring_task():
    """Test removing recurring tasks."""
    manager = RecurringTaskManager()

    base_task = Task(title="Test task", priority=TaskPriority.MEDIUM)
    future_date = (datetime.now() + timedelta(days=1)).isoformat()
    recurring_task = RecurringTask(
        base_task=base_task,
        recurrence_rule=RecurrenceRule.DAILY,
        next_occurrence=future_date
    )

    manager.add_recurring_task(recurring_task)
    assert len(manager.recurring_tasks) == 1

    # Remove the task
    result = manager.remove_recurring_task(recurring_task.id)
    assert result is True
    assert len(manager.recurring_tasks) == 0

    # Try to remove a non-existent task
    result = manager.remove_recurring_task("non-existent")
    assert result is False


def test_get_recurring_task():
    """Test getting a specific recurring task."""
    manager = RecurringTaskManager()

    base_task = Task(title="Test task", priority=TaskPriority.MEDIUM)
    future_date = (datetime.now() + timedelta(days=1)).isoformat()
    recurring_task = RecurringTask(
        base_task=base_task,
        recurrence_rule=RecurrenceRule.DAILY,
        next_occurrence=future_date
    )

    manager.add_recurring_task(recurring_task)

    # Get the task
    retrieved_task = manager.get_recurring_task(recurring_task.id)
    assert retrieved_task is not None
    assert retrieved_task.id == recurring_task.id

    # Try to get a non-existent task
    retrieved_task = manager.get_recurring_task("non-existent")
    assert retrieved_task is None


def test_process_inactive_recurring_task():
    """Test that inactive recurring tasks don't generate new tasks."""
    manager = RecurringTaskManager()

    base_task = Task(title="Test task", priority=TaskPriority.MEDIUM)
    future_date = (datetime.now() + timedelta(days=1)).isoformat()
    recurring_task = RecurringTask(
        base_task=base_task,
        recurrence_rule=RecurrenceRule.DAILY,
        next_occurrence=future_date
    )

    # Make the task inactive
    recurring_task.is_active = False

    manager.add_recurring_task(recurring_task)

    # Process recurring tasks - this should not generate any new tasks
    new_tasks = manager.process_recurring_tasks()
    assert len(new_tasks) == 0

    # Now make it active and simulate that time has passed
    recurring_task.is_active = True
    past_date = (datetime.now() - timedelta(minutes=1)).isoformat()
    recurring_task._next_occurrence = past_date  # Bypass validation for testing

    # Now it should generate a task
    new_tasks = manager.process_recurring_tasks()
    assert len(new_tasks) == 1

    # Set it back to inactive and process again
    recurring_task.is_active = False
    new_tasks = manager.process_recurring_tasks()
    assert len(new_tasks) == 0


def test_multiple_recurring_tasks():
    """Test processing multiple recurring tasks."""
    manager = RecurringTaskManager()

    base_task1 = Task(title="Task 1", priority=TaskPriority.MEDIUM)
    base_task2 = Task(title="Task 2", priority=TaskPriority.LOW)

    # Create two recurring tasks with future dates initially
    future_date = (datetime.now() + timedelta(days=1)).isoformat()
    recurring_task1 = RecurringTask(
        base_task=base_task1,
        recurrence_rule=RecurrenceRule.DAILY,
        next_occurrence=future_date
    )
    recurring_task2 = RecurringTask(
        base_task=base_task2,
        recurrence_rule=RecurrenceRule.WEEKLY,
        next_occurrence=future_date
    )

    manager.add_recurring_task(recurring_task1)
    manager.add_recurring_task(recurring_task2)

    # Initially, no tasks should be generated since dates are in the future
    new_tasks = manager.process_recurring_tasks()
    assert len(new_tasks) == 0

    # Now simulate that time has passed for both tasks
    past_date = (datetime.now() - timedelta(minutes=2)).isoformat()
    recurring_task1._next_occurrence = past_date  # Bypass validation for testing
    recurring_task2._next_occurrence = past_date  # Bypass validation for testing

    # Process recurring tasks - both should generate now
    new_tasks = manager.process_recurring_tasks()
    assert len(new_tasks) == 2

    titles = [task.title for task in new_tasks]
    assert "Task 1" in titles
    assert "Task 2" in titles