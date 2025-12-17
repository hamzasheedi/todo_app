"""
User interface utilities for the Todo CLI application.

This module provides functions for displaying tasks and other UI elements.
"""
from typing import List
from core.task import Task


def display_task(task: Task) -> str:
    """
    Format a task for display.

    Args:
        task: Task object to format

    Returns:
        Formatted string representation of the task
    """
    status_icon = "✓" if task.status.name.lower() == 'complete' else "○"
    priority_char = task.priority.name[0]  # 'H', 'M', 'L'
    tags_str = f" [{', '.join(task.tags)}]" if task.tags else ""
    due_str = f" (due: {task.due_date})" if task.due_date else ""

    return f"{status_icon} [{priority_char}] {task.title}{tags_str}{due_str}"


def display_tasks(tasks: List[Task], show_index: bool = True) -> None:
    """
    Display a list of tasks with both display number and ID.

    Args:
        tasks: List of Task objects to display
        show_index: Whether to show index numbers
    """
    if not tasks:
        print("No tasks found.")
        return

    for i, task in enumerate(tasks, 1):
        if show_index:
            print(f"{i:2d}. {display_task(task)} [ID: {task.id[:8]}...]")
        else:
            print(f"    {display_task(task)} [ID: {task.id[:8]}...]")


def display_task_details(task: Task) -> None:
    """
    Display detailed information about a single task.

    Args:
        task: Task object to display details for
    """
    print(f"Title: {task.title}")
    print(f"Description: {task.description or 'None'}")
    print(f"Status: {task.status.name.title()}")
    print(f"Priority: {task.priority.name.title()}")
    print(f"Tags: {', '.join(task.tags) if task.tags else 'None'}")
    print(f"Due Date: {task.due_date or 'None'}")
    print(f"Created: {task.created_date}")
    print(f"Updated: {task.updated_date}")
    print(f"ID: {task.id}")