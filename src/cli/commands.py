"""
Command handlers for the Todo CLI application.

This module contains all the command handlers for the CLI interface.
"""
from typing import Optional, List
from core.task import Task, TaskPriority
from storage.json_storage import JSONStorage
from utils.config import get_config


class TaskManager:
    """
    Manager class for handling task operations.
    """
    def __init__(self):
        """Initialize the task manager with storage."""
        self.storage = JSONStorage()

    def add_task(self, title: str, description: Optional[str] = None,
                 priority: Optional[str] = None, tags: Optional[List[str]] = None,
                 due_date: Optional[str] = None) -> Task:
        """
        Add a new task to the system.

        Args:
            title: Task title (1-200 characters)
            description: Task description (0-1000 characters, optional)
            priority: Task priority ('low', 'medium', 'high', optional)
            tags: List of tags (0-10 tags, optional)
            due_date: Due date in ISO 8601 format (optional)

        Returns:
            The created Task object

        Raises:
            ValueError: If validation fails (empty title, invalid priority, duplicate task)
        """
        # Check for empty title (Edge Case #127)
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty or contain only whitespace")

        # Check for duplicate task (Edge Case #134)
        # Look for existing tasks with the same title
        existing_tasks = self.storage.load_tasks()
        for task in existing_tasks:
            if task.title.strip().lower() == title.strip().lower():
                raise ValueError(f"A task with title '{title}' already exists")

        # Convert priority string to enum if provided
        priority_enum = None
        if priority:
            try:
                priority_enum = TaskPriority(priority.lower())
            except ValueError:
                raise ValueError(f"Invalid priority: {priority}. Must be 'low', 'medium', or 'high'.")

        # Use default priority if not provided
        if priority_enum is None:
            config = get_config()
            default_priority_str = config.get("default_priority", "medium")
            priority_enum = TaskPriority(default_priority_str)

        # Create the task using the factory method
        task = Task.create(
            title=title,
            description=description,
            priority=priority_enum,
            tags=tags,
            due_date=due_date
        )

        # Save to storage
        self.storage.add_task(task)

        return task

    def view_tasks(self, status: Optional[str] = None, priority: Optional[str] = None,
                   tag: Optional[str] = None) -> List[Task]:
        """
        Get all tasks, optionally filtered by status, priority, or tag.

        Args:
            status: Filter by status ('complete', 'incomplete', 'all')
            priority: Filter by priority ('low', 'medium', 'high')
            tag: Filter by tag

        Returns:
            List of Task objects matching the filters
        """
        tasks = self.storage.load_tasks()

        # Apply filters
        if status and status.lower() != 'all':
            if status.lower() == 'complete':
                tasks = [task for task in tasks if task.status.name.lower() == 'complete']
            elif status.lower() == 'incomplete':
                tasks = [task for task in tasks if task.status.name.lower() == 'incomplete']

        if priority:
            try:
                priority_enum = TaskPriority(priority.lower())
                tasks = [task for task in tasks if task.priority == priority_enum]
            except ValueError:
                raise ValueError(f"Invalid priority: {priority}")

        if tag:
            tasks = [task for task in tasks if tag in task.tags]

        return tasks

    def filter_tasks(self, filters: Optional[dict] = None) -> List[Task]:
        """
        Filter tasks based on multiple criteria.

        Args:
            filters: Dictionary containing filter criteria
                     Possible keys: status, priority, tags, due_date
                     Example: {
                         'status': 'complete',
                         'priority': 'high',
                         'tags': ['work', 'urgent']
                     }

        Returns:
            List of Task objects matching all filter criteria
        """
        if not filters:
            return self.storage.load_tasks()

        tasks = self.storage.load_tasks()

        # Apply status filter
        if 'status' in filters and filters['status'] and filters['status'].lower() != 'all':
            status_val = filters['status'].lower()
            if status_val == 'complete':
                tasks = [task for task in tasks if task.status.name.lower() == 'complete']
            elif status_val == 'incomplete':
                tasks = [task for task in tasks if task.status.name.lower() == 'incomplete']

        # Apply priority filter
        if 'priority' in filters and filters['priority']:
            try:
                priority_enum = TaskPriority(filters['priority'].lower())
                tasks = [task for task in tasks if task.priority == priority_enum]
            except ValueError:
                raise ValueError(f"Invalid priority: {filters['priority']}")

        # Apply tags filter - task must have ALL specified tags
        if 'tags' in filters and filters['tags']:
            required_tags = filters['tags'] if isinstance(filters['tags'], list) else [filters['tags']]
            tasks = [task for task in tasks if all(tag in task.tags for tag in required_tags)]

        # Apply due date filter (contains specific date)
        if 'due_date' in filters and filters['due_date']:
            due_date_val = filters['due_date']
            tasks = [task for task in tasks if task.due_date and due_date_val in task.due_date]

        return tasks

    def sort_tasks(self, tasks: List[Task], sort_by: str = 'priority', reverse: bool = False) -> List[Task]:
        """
        Sort tasks based on specified criteria.

        Args:
            tasks: List of tasks to sort
            sort_by: Criteria to sort by ('priority', 'due_date', 'alphabetical')
            reverse: Whether to sort in reverse order

        Returns:
            List of sorted Task objects
        """
        if sort_by.lower() == 'priority':
            # Sort by priority: high -> medium -> low
            priority_order = {TaskPriority.HIGH: 0, TaskPriority.MEDIUM: 1, TaskPriority.LOW: 2}
            return sorted(tasks, key=lambda task: priority_order[task.priority], reverse=reverse)

        elif sort_by.lower() == 'due_date':
            # Sort by due date (None values last)
            def due_date_key(task):
                if task.due_date is None:
                    # Use a value that sorts after all dates when reverse=False,
                    # and before all dates when reverse=True
                    # Using a tuple where the first element ensures proper placement
                    return (1, '') if not reverse else (-1, '')  # 1 means it goes last when not reversed
                return (0, task.due_date, task.title)  # 0 means it comes first, then by due date, then by title

            return sorted(tasks, key=due_date_key, reverse=reverse)

        elif sort_by.lower() == 'alphabetical':
            # Sort alphabetically by title
            return sorted(tasks, key=lambda task: task.title.lower(), reverse=reverse)

        else:
            # Default to priority if invalid sort_by provided
            priority_order = {TaskPriority.HIGH: 0, TaskPriority.MEDIUM: 1, TaskPriority.LOW: 2}
            return sorted(tasks, key=lambda task: priority_order[task.priority], reverse=reverse)

    def get_sorted_tasks(self, sort_by: str = 'priority', filters: Optional[dict] = None,
                         reverse: bool = False) -> List[Task]:
        """
        Get tasks that are filtered and sorted.

        Args:
            sort_by: Criteria to sort by ('priority', 'due_date', 'alphabetical')
            filters: Dictionary containing filter criteria
            reverse: Whether to sort in reverse order

        Returns:
            List of filtered and sorted Task objects
        """
        # First apply filters
        tasks = self.filter_tasks(filters)

        # Then sort the filtered tasks
        return self.sort_tasks(tasks, sort_by, reverse)

    def update_task(self, task_id: str, title: Optional[str] = None,
                    description: Optional[str] = None, status: Optional[str] = None,
                    priority: Optional[str] = None, tags: Optional[List[str]] = None,
                    due_date: Optional[str] = None) -> bool:
        """
        Update an existing task.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
            status: New status ('complete', 'incomplete', optional)
            priority: New priority ('low', 'medium', 'high', optional)
            tags: New tags (optional)
            due_date: New due date (optional)

        Returns:
            True if task was updated, False if task not found
        """
        # Get the existing task
        existing_task = self.storage.get_task(task_id)
        if not existing_task:
            return False

        # Create updated task with new values or existing values
        updated_task = Task(
            id=existing_task.id,
            title=title if title is not None else existing_task.title,
            description=description if description is not None else existing_task.description,
            status=existing_task.status,
            priority=existing_task.priority,
            tags=existing_task.tags,
            due_date=existing_task.due_date,
            created_date=existing_task.created_date,
            updated_date=existing_task.updated_date  # This will be overridden by setters if fields change
        )

        # Update specific fields if provided
        if title is not None:
            updated_task.title = title
        if description is not None:
            updated_task.description = description
        if status is not None:
            from core.task import TaskStatus
            if status.lower() == 'complete':
                updated_task.status = TaskStatus.COMPLETE
            elif status.lower() == 'incomplete':
                updated_task.status = TaskStatus.INCOMPLETE
            else:
                raise ValueError(f"Invalid status: {status}. Must be 'complete' or 'incomplete'.")
        if priority is not None:
            try:
                updated_task.priority = TaskPriority(priority.lower())
            except ValueError:
                raise ValueError(f"Invalid priority: {priority}")
        if tags is not None:
            updated_task.tags = tags
        if due_date is not None:
            updated_task.due_date = due_date

        # Save the updated task
        return self.storage.update_task(task_id, updated_task)

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if task was deleted, False if task not found
        """
        return self.storage.delete_task(task_id)

    def delete_task_with_feedback(self, task_id: str) -> bool:
        """
        Delete a task by ID with user feedback.

        This method provides user-friendly feedback when deleting tasks,
        including showing available tasks if the specified task doesn't exist (FR-016).

        Args:
            task_id: ID of the task to delete

        Returns:
            True if task was deleted, False if task not found
        """
        # Check if task exists before attempting deletion
        task_exists = self.storage.task_exists(task_id)

        if not task_exists:
            print(f"Error: Task with ID '{task_id}' not found.")

            # Show available tasks (FR-016)
            all_tasks = self.storage.load_tasks()
            if all_tasks:
                print("Available tasks:")
                from cli.ui import display_tasks
                display_tasks(all_tasks)
            else:
                print("No tasks available.")

            return False

        # Task exists, proceed with deletion
        result = self.storage.delete_task(task_id)
        if result:
            print(f"Task '{task_id}' deleted successfully.")

        return result

    def mark_task_status(self, task_id: str, status: str) -> bool:
        """
        Mark a task as complete or incomplete.

        Args:
            task_id: ID of the task to update
            status: New status ('complete' or 'incomplete')

        Returns:
            True if task status was updated, False if task not found or invalid status
        """
        # Get the existing task
        existing_task = self.storage.get_task(task_id)
        if not existing_task:
            return False

        # Determine the new status
        from core.task import TaskStatus
        try:
            if status.lower() == 'complete':
                new_status = TaskStatus.COMPLETE
            elif status.lower() == 'incomplete':
                new_status = TaskStatus.INCOMPLETE
            else:
                return False  # Return False for invalid status
        except AttributeError:
            return False  # Return False if status is not a string

        # Create updated task with new status
        updated_task = Task(
            id=existing_task.id,
            title=existing_task.title,
            description=existing_task.description,
            status=new_status,
            priority=existing_task.priority,
            tags=existing_task.tags,
            due_date=existing_task.due_date,
            created_date=existing_task.created_date,
            updated_date=existing_task.updated_date
        )

        # Save the updated task
        return self.storage.update_task(task_id, updated_task)

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a specific task by ID or display number.

        Implements T005: UX & Error Handling framework - consistent task identification
        that accepts the same identifier format that is displayed.

        Args:
            task_id: ID of the task to retrieve (can be UUID or display number)

        Returns:
            Task object if found, None otherwise
        """
        # First try to get by UUID
        task = self.storage.get_task(task_id)
        if task:
            return task

        # If not found by UUID, check if it's a display number
        try:
            display_number = int(task_id)
            all_tasks = self.storage.load_tasks()
            if 1 <= display_number <= len(all_tasks):
                return all_tasks[display_number - 1]  # Display numbers start from 1
        except ValueError:
            # Not a valid number, so it's not a display number
            pass

        return None

    def get_task_by_display_number(self, display_number: int) -> Optional[Task]:
        """
        Get a specific task by its display number (1-indexed).

        Args:
            display_number: The display number of the task (1-indexed)

        Returns:
            Task object if found, None otherwise
        """
        all_tasks = self.storage.load_tasks()
        if 1 <= display_number <= len(all_tasks):
            return all_tasks[display_number - 1]  # Display numbers start from 1
        return None

    def get_all_tasks_with_numbers(self) -> List[tuple]:
        """
        Get all tasks with their display numbers.

        Returns:
            List of tuples containing (display_number, task)
        """
        all_tasks = self.storage.load_tasks()
        return [(i + 1, task) for i, task in enumerate(all_tasks)]

    def update_task_priority(self, task_id: str, priority: str) -> bool:
        """
        Update the priority of a task.

        Args:
            task_id: ID of the task to update
            priority: New priority ('low', 'medium', 'high')

        Returns:
            True if task was updated, False if task not found
        """
        return self.update_task(task_id, priority=priority)

    def update_task_tags(self, task_id: str, tags: List[str]) -> bool:
        """
        Update the tags of a task.

        Args:
            task_id: ID of the task to update
            tags: New list of tags

        Returns:
            True if task was updated, False if task not found
        """
        return self.update_task(task_id, tags=tags)

    def add_tag_to_task(self, task_id: str, tag: str) -> bool:
        """
        Add a single tag to a task.

        Args:
            task_id: ID of the task to update
            tag: Tag to add

        Returns:
            True if task was updated, False if task not found
        """
        task = self.get_task(task_id)
        if not task:
            return False

        # Create new tag list with the new tag added
        new_tags = task.tags.copy()
        if tag not in new_tags:
            new_tags.append(tag)

        return self.update_task(task_id, tags=new_tags)

    def remove_tag_from_task(self, task_id: str, tag: str) -> bool:
        """
        Remove a single tag from a task.

        Args:
            task_id: ID of the task to update
            tag: Tag to remove

        Returns:
            True if task was updated, False if task not found
        """
        task = self.get_task(task_id)
        if not task:
            return False

        # Create new tag list without the specified tag
        new_tags = [t for t in task.tags if t != tag]

        return self.update_task(task_id, tags=new_tags)

    def clear_all_tasks(self) -> None:
        """
        Clear all tasks from storage.
        """
        self.storage.clear_all_tasks()

    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Search tasks by keyword in title or description.

        Args:
            keyword: Keyword to search for

        Returns:
            List of tasks that match the search criteria
        """
        all_tasks = self.storage.load_tasks()
        keyword_lower = keyword.lower()

        matching_tasks = []
        for task in all_tasks:
            # Check if keyword is in title or description (if description exists)
            if (keyword_lower in task.title.lower() or
                (task.description and keyword_lower in task.description.lower())):
                matching_tasks.append(task)

        return matching_tasks


# Global task manager instance
_task_manager: Optional[TaskManager] = None


def get_task_manager() -> TaskManager:
    """
    Get the global task manager instance.

    Returns:
        TaskManager instance
    """
    global _task_manager
    if _task_manager is None:
        _task_manager = TaskManager()
    return _task_manager


def update_task_priority(task_id: str, priority: str) -> bool:
    """
    Update the priority of a task.

    Args:
        task_id: ID of the task to update
        priority: New priority ('low', 'medium', 'high')

    Returns:
        True if task was updated, False if task not found
    """
    task_manager = get_task_manager()
    return task_manager.update_task_priority(task_id, priority)


def update_task_tags(task_id: str, tags: List[str]) -> bool:
    """
    Update the tags of a task.

    Args:
        task_id: ID of the task to update
        tags: New list of tags

    Returns:
        True if task was updated, False if task not found
    """
    task_manager = get_task_manager()
    return task_manager.update_task_tags(task_id, tags)


def add_tag_to_task(task_id: str, tag: str) -> bool:
    """
    Add a single tag to a task.

    Args:
        task_id: ID of the task to update
        tag: Tag to add

    Returns:
        True if task was updated, False if task not found
    """
    task_manager = get_task_manager()
    return task_manager.add_tag_to_task(task_id, tag)


def remove_tag_from_task(task_id: str, tag: str) -> bool:
    """
    Remove a single tag from a task.

    Args:
        task_id: ID of the task to update
        tag: Tag to remove

    Returns:
        True if task was updated, False if task not found
    """
    task_manager = get_task_manager()
    return task_manager.remove_tag_from_task(task_id, tag)


def search_tasks(keyword: str) -> List[Task]:
    """
    Search tasks by keyword in title or description.

    Args:
        keyword: Keyword to search for

    Returns:
        List of tasks that match the search criteria
    """
    task_manager = get_task_manager()
    return task_manager.search_tasks(keyword)


def filter_tasks(filters: Optional[dict] = None) -> List[Task]:
    """
    Filter tasks based on multiple criteria.

    Args:
        filters: Dictionary containing filter criteria
                 Possible keys: status, priority, tags, due_date

    Returns:
        List of tasks that match the filter criteria
    """
    task_manager = get_task_manager()
    return task_manager.filter_tasks(filters)


def sort_tasks(tasks: List[Task], sort_by: str = 'priority', reverse: bool = False) -> List[Task]:
    """
    Sort tasks based on specified criteria.

    Args:
        tasks: List of tasks to sort
        sort_by: Criteria to sort by ('priority', 'due_date', 'alphabetical')
        reverse: Whether to sort in reverse order

    Returns:
        List of sorted tasks
    """
    task_manager = get_task_manager()
    return task_manager.sort_tasks(tasks, sort_by, reverse)


def get_sorted_tasks(sort_by: str = 'priority', filters: Optional[dict] = None,
                     reverse: bool = False) -> List[Task]:
    """
    Get tasks that are filtered and sorted.

    Args:
        sort_by: Criteria to sort by ('priority', 'due_date', 'alphabetical')
        filters: Dictionary containing filter criteria
        reverse: Whether to sort in reverse order

    Returns:
        List of filtered and sorted tasks
    """
    task_manager = get_task_manager()
    return task_manager.get_sorted_tasks(sort_by, filters, reverse)


def add_task(title: str, description: Optional[str] = None,
             priority: Optional[str] = None, tags: Optional[List[str]] = None,
             due_date: Optional[str] = None) -> Task:
    """
    Add a new task to the system.

    Args:
        title: Task title (1-200 characters)
        description: Task description (0-1000 characters, optional)
        priority: Task priority ('low', 'medium', 'high', optional)
        tags: List of tags (0-10 tags, optional)
        due_date: Due date in ISO 8601 format (optional)

    Returns:
        The created Task object

    Raises:
        ValueError: If validation fails
    """
    task_manager = get_task_manager()
    return task_manager.add_task(title, description, priority, tags, due_date)


def view_tasks(status: Optional[str] = None, priority: Optional[str] = None,
               tag: Optional[str] = None) -> List[Task]:
    """
    Get all tasks, optionally filtered by status, priority, or tag.

    Args:
        status: Filter by status ('complete', 'incomplete', 'all')
        priority: Filter by priority ('low', 'medium', 'high')
        tag: Filter by tag

    Returns:
        List of Task objects matching the filters
    """
    task_manager = get_task_manager()
    return task_manager.view_tasks(status, priority, tag)


def update_task(task_id: str, title: Optional[str] = None,
                description: Optional[str] = None, status: Optional[str] = None,
                priority: Optional[str] = None, tags: Optional[List[str]] = None,
                due_date: Optional[str] = None) -> bool:
    """
    Update an existing task.

    Args:
        task_id: ID of the task to update
        title: New title (optional)
        description: New description (optional)
        status: New status ('complete', 'incomplete', optional)
        priority: New priority ('low', 'medium', 'high', optional)
        tags: New tags (optional)
        due_date: New due date (optional)

    Returns:
        True if task was updated, False if task not found
    """
    task_manager = get_task_manager()
    return task_manager.update_task(task_id, title, description, status, priority, tags, due_date)


def delete_task(task_id: str) -> bool:
    """
    Delete a task by ID.

    Args:
        task_id: ID of the task to delete

    Returns:
        True if task was deleted, False if task not found
    """
    task_manager = get_task_manager()
    return task_manager.delete_task(task_id)


def mark_task_status(task_id: str, status: str) -> bool:
    """
    Mark a task as complete or incomplete.

    Args:
        task_id: ID of the task to update
        status: New status ('complete' or 'incomplete')

    Returns:
        True if task status was updated, False if task not found
    """
    task_manager = get_task_manager()
    return task_manager.mark_task_status(task_id, status)


def get_task(task_id: str) -> Optional[Task]:
    """
    Get a specific task by ID.

    Args:
        task_id: ID of the task to retrieve

    Returns:
        Task object if found, None otherwise
    """
    task_manager = get_task_manager()
    return task_manager.get_task(task_id)


def create_recurring_task(title: str, description: Optional[str] = None,
                         priority: Optional[str] = None, tags: Optional[List[str]] = None,
                         due_date: Optional[str] = None, recurrence_rule: str = 'daily',
                         next_occurrence: Optional[str] = None, end_date: Optional[str] = None,
                         continue_after_completion: Optional[str] = 'always_continue') -> Optional['RecurringTask']:
    """
    Create a new recurring task.

    Args:
        title: Task title (1-200 characters)
        description: Task description (0-1000 characters, optional)
        priority: Task priority ('low', 'medium', 'high', optional)
        tags: List of tags (0-10 tags, optional)
        due_date: Due date in ISO 8601 format (optional)
        recurrence_rule: How often the task should repeat ('daily', 'weekly', 'monthly', 'yearly')
        next_occurrence: When the first instance should occur (ISO 8601 format)
        end_date: When the recurrence should end (ISO 8601 format, optional)
        continue_after_completion: Policy for continuing after completion ('always_continue', 'prompt_user', 'stop_if_completed')

    Returns:
        The created RecurringTask object if successful, None otherwise
    """
    from core.task import Task, TaskPriority
    from core.recurring_task import RecurringTask, RecurrenceRule, ContinuePolicy
    from datetime import datetime

    # Create the base task
    priority_enum = None
    if priority:
        try:
            priority_enum = TaskPriority(priority.lower())
        except ValueError:
            raise ValueError(f"Invalid priority: {priority}. Must be 'low', 'medium', or 'high'.")

    # Use default priority if not provided
    if priority_enum is None:
        config = get_config()
        default_priority_str = config.get("default_priority", "medium")
        priority_enum = TaskPriority(default_priority_str)

    base_task = Task.create(
        title=title,
        description=description,
        priority=priority_enum,
        tags=tags,
        due_date=due_date
    )

    # Parse recurrence rule
    try:
        rule_enum = RecurrenceRule(recurrence_rule.lower())
    except ValueError:
        raise ValueError(f"Invalid recurrence rule: {recurrence_rule}. Must be 'daily', 'weekly', 'monthly', or 'yearly'.")

    # Use current time as next occurrence if not provided
    if not next_occurrence:
        next_occurrence = datetime.now().isoformat()

    # Parse continuation policy
    try:
        continue_policy = ContinuePolicy(continue_after_completion.lower())
    except ValueError:
        raise ValueError(f"Invalid continue policy: {continue_after_completion}. Must be 'always_continue', 'prompt_user', or 'stop_if_completed'.")

    # Create recurring task
    recurring_task = RecurringTask(
        base_task=base_task,
        recurrence_rule=rule_enum,
        next_occurrence=next_occurrence,
        end_date=end_date,
        continue_after_completion=continue_policy
    )

    # In a real implementation, we would save this to a recurring tasks storage
    # For now, we'll just return the object
    return recurring_task


def create_reminder(task_id: str, reminder_time: str) -> Optional['Reminder']:
    """
    Create a new reminder for a task.

    Args:
        task_id: ID of the task to create a reminder for
        reminder_time: When to trigger the reminder (ISO 8601 format)

    Returns:
        The created Reminder object if successful, None otherwise
    """
    from core.reminder import Reminder
    from utils.validators import validate_iso_datetime

    # Validate the reminder time
    if not validate_iso_datetime(reminder_time):
        raise ValueError(f"Invalid ISO 8601 datetime format: {reminder_time}")

    # Check if it's a future time
    from datetime import datetime
    reminder_dt = datetime.fromisoformat(reminder_time.replace('Z', '+00:00'))
    if reminder_dt < datetime.now():
        raise ValueError("Reminder time must be in the future")

    # Create the reminder
    reminder = Reminder(
        task_id=task_id,
        reminder_time=reminder_time
    )

    # In a real implementation, we would save this to a reminders storage
    # For now, we'll just return the object
    return reminder