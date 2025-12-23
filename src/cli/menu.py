"""
Interactive menu system for the Todo CLI application.

This module provides an interactive menu-driven interface for the todo application.
"""
import sys
from typing import Optional
from cli.commands import TaskManager, get_task_manager
from cli.ui import display_tasks, display_task, display_task_details
from core.task import TaskPriority
from core.recurring_task import RecurrenceRule, ContinuePolicy
from core.reminder import ReminderStatus
from utils.validators import validate_iso_datetime


def get_user_input(prompt: str) -> str:
    """
    Get input from the user with a prompt.

    Args:
        prompt: The prompt to display to the user

    Returns:
        The user's input as a string
    """
    return input(prompt).strip()


def get_valid_menu_choice() -> str:
    """
    Get a valid menu choice from the user with retry behavior.

    Implements T005: UX & Error Handling framework - retry-safe input handling
    for menu navigation. Invalid input triggers re-prompt, not menu reset.

    Returns:
        The user's valid menu choice as a string
    """
    while True:
        choice = input("\nSelect an option (1-20): ").strip()
        if choice.lower() in ["quit", "exit"]:
            return "20"
        if choice in [str(i) for i in range(1, 21)]:
            return choice
        print("Invalid choice. Please select a number between 1-20.")


def get_valid_task_id(task_manager: TaskManager, prompt: str = "Enter task ID or display number: ") -> Optional[str]:
    """
    Get a valid task ID from the user with retry behavior, accepting both UUID and display number.

    Implements T005: UX & Error Handling framework - consistent task identification
    that accepts the same identifier format that is displayed.

    Args:
        task_manager: TaskManager instance to check task existence
        prompt: The prompt to display to the user

    Returns:
        The valid task ID (UUID) if found, None if user cancels or no tasks exist
    """
    all_tasks = task_manager.view_tasks()
    if not all_tasks:
        print("No tasks available.")
        return None

    while True:
        task_input = get_user_input(prompt)
        if not task_input:
            print("Task ID cannot be empty. Please enter a valid ID or display number.")
            continue

        # Try to get the task using the flexible get_task method
        task = task_manager.get_task(task_input)
        if task:
            return task.id  # Return the actual UUID
        else:
            print(f"Task with ID or display number '{task_input}' not found.")
            print("Available tasks:")
            display_tasks(all_tasks)
            print("Please try again or press Ctrl+C to cancel.")


def get_task_details_from_user() -> tuple:
    """
    Prompt the user for task details with retry-safe validation and context preservation.

    Implements T005: UX & Error Handling framework - retry-safe input handling
    and context preservation during multi-step task creation.

    Returns:
        A tuple containing (title, description, priority, tags, due_date)
    """
    print("\n--- Add New Task ---")

    # Store previously entered values to preserve context
    title = None
    description = None
    priority = "medium"  # default
    tags = None
    due_date = None

    # Get title with validation retry
    while title is None or title.strip() == "":
        title = get_user_input("Enter task title: ")
        if not title or not title.strip():
            print("Error: Task title cannot be empty. Please enter a valid title.")

    description = get_user_input("Enter task description (optional, press Enter to skip): ")
    if not description:
        description = None

    # Get priority with validation retry
    priority_map = {"1": "high", "2": "medium", "3": "low"}
    priority_choice = ""
    while priority_choice not in priority_map:
        print("Select priority (1-3):")
        print("1. High")
        print("2. Medium")
        print("3. Low")
        priority_choice = get_user_input("Enter choice (1-3, default is 2): ")
        if priority_choice == "":
            priority_choice = "2"  # default
            break
        if priority_choice not in priority_map:
            print("Invalid choice. Please enter 1, 2, or 3.")

    priority = priority_map.get(priority_choice, "medium")

    tags_input = get_user_input("Enter tags separated by commas (optional, press Enter to skip): ")
    tags = None
    if tags_input:
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

    # Get due date with validation retry
    due_date = get_user_input("Enter due date (YYYY-MM-DD or ISO format, optional, press Enter to skip): ")
    if due_date:
        # Validate the date format
        while due_date and not validate_iso_datetime(due_date):
            print(f"Error: Invalid date format '{due_date}'. Please use YYYY-MM-DD (e.g., 2025-12-31) or ISO datetime format.")
            due_date = get_user_input("Enter due date (YYYY-MM-DD or ISO format, optional, press Enter to skip): ")
            if not due_date:
                break
    else:
        due_date = None

    return title, description, priority, tags, due_date


def run_menu():
    """
    Run the main interactive menu loop.
    """
    print("Welcome to the Todo CLI Application!")
    print("Type 'help' for available commands or 'quit' to exit.\n")

    task_manager = get_task_manager()

    while True:
        try:
            print("\n--- Main Menu ---")
            print("1. View all tasks")
            print("2. Add new task")
            print("3. Update task")
            print("4. Delete task")
            print("5. Mark task as complete")
            print("6. Mark task as incomplete")
            print("7. View tasks by status")
            print("8. View tasks by priority")
            print("9. Search tasks")
            print("10. Filter tasks")
            print("11. Sort tasks")
            print("12. Update task priority")
            print("13. Update task tags")
            print("14. Add tag to task")
            print("15. Remove tag from task")
            print("16. Add recurring task")
            print("17. Add reminder")
            print("18. View recurring tasks")
            print("19. View reminders")
            print("20. Exit")
            print("------------------")

            # Get user input and check for global commands
            user_input = get_user_input("\nSelect an option (1-20) or type 'help'/'quit': ").strip()

            if user_input.lower() == 'help':
                print("\n--- Help ---")
                print("Commands available:")
                print("- 1-20: Menu options")
                print("- help: Show this help message")
                print("- quit: Exit the application")
                print("- exit: Exit the application")
                print("- Ctrl+C: Interrupt current operation")
                continue
            elif user_input.lower() in ['quit', 'exit']:
                print("Thank you for using the Todo CLI Application. Goodbye!")
                sys.exit(0)
            elif user_input in [str(i) for i in range(1, 21)]:
                choice = user_input
            else:
                print("Invalid choice. Please select a number between 1-20, or type 'help' for assistance.")
                continue

            if choice == "1":
                view_all_tasks(task_manager)
            elif choice == "2":
                add_new_task(task_manager)
            elif choice == "3":
                update_existing_task(task_manager)
            elif choice == "4":
                delete_existing_task(task_manager)
            elif choice == "5":
                mark_task_complete(task_manager)
            elif choice == "6":
                mark_task_incomplete(task_manager)
            elif choice == "7":
                view_tasks_by_status(task_manager)
            elif choice == "8":
                view_tasks_by_priority(task_manager)
            elif choice == "9":
                search_tasks(task_manager)
            elif choice == "10":
                filter_tasks_menu(task_manager)
            elif choice == "11":
                sort_tasks_menu(task_manager)
            elif choice == "12":
                update_task_priority(task_manager)
            elif choice == "13":
                update_task_tags(task_manager)
            elif choice == "14":
                add_tag_to_task(task_manager)
            elif choice == "15":
                remove_tag_from_task(task_manager)
            elif choice == "16":
                add_recurring_task(task_manager)
            elif choice == "17":
                add_reminder(task_manager)
            elif choice == "18":
                list_recurring_tasks()
            elif choice == "19":
                list_reminders()
            elif choice == "20":
                print("Thank you for using the Todo CLI Application. Goodbye!")
                sys.exit(0)
        except KeyboardInterrupt:
            print("\n\nOperation interrupted by user. Returning to main menu.")
            continue  # Return to main menu instead of exiting
        except Exception as e:
            print(f"An error occurred: {e}")


def view_all_tasks(task_manager: TaskManager):
    """View all tasks."""
    print("\n--- All Tasks ---")
    tasks = task_manager.view_tasks()
    if not tasks:
        print("No tasks found.")
    else:
        display_tasks(tasks)


def add_new_task(task_manager: TaskManager):
    """Add a new task."""
    try:
        title, description, priority, tags, due_date = get_task_details_from_user()
        task = task_manager.add_task(title, description, priority, tags, due_date)
        print(f"\nTask '{task.title}' added successfully with ID: {task.id}")
    except ValueError as e:
        print(f"Error adding task: {e}")
    except Exception as e:
        print(f"Unexpected error adding task: {e}")


def update_existing_task(task_manager: TaskManager):
    """Update an existing task with retry-safe validation and context preservation."""
    print("\n--- Update Task ---")
    task_id = get_valid_task_id(task_manager, "Enter task ID or display number to update: ")
    if not task_id:
        return

    # First, check if the task exists and display its current details
    task = task_manager.get_task(task_id)
    if not task:
        print(f"Task with ID '{task_id}' not found.")
        return

    print(f"\nCurrent task details:")
    display_task_details(task)

    print("\nEnter new values (press Enter to keep current value):")
    new_title = get_user_input(f"New title (current: '{task.title}'): ")
    new_title = new_title if new_title else None

    new_description = get_user_input(f"New description (current: '{task.description}'): ")
    new_description = new_description if new_description else None

    print("New priority (1: High, 2: Medium, 3: Low, Enter: keep current):")
    priority_choice = get_user_input(f"Current: {task.priority.name.title()} ")
    priority_map = {"1": "high", "2": "medium", "3": "low"}
    new_priority = None
    if priority_choice:
        if priority_choice in priority_map:
            new_priority = priority_map[priority_choice]
        else:
            print("Invalid choice. Priority not updated.")
    # If priority_choice is empty, new_priority remains None (no change)

    # Process tags
    current_tags = ", ".join(task.tags) if task.tags else ""
    new_tags_input = get_user_input(f"New tags (comma-separated, current: '{current_tags}'): ")
    new_tags = None
    if new_tags_input:
        new_tags = [tag.strip() for tag in new_tags_input.split(",") if tag.strip()]
    elif new_tags_input == "":  # User pressed enter to clear tags
        new_tags = []

    # Get due date with validation retry
    new_due_date = get_user_input(f"New due date (current: '{task.due_date}'): ")
    if new_due_date:
        # Validate the date format
        while new_due_date and not validate_iso_datetime(new_due_date):
            print(f"Error: Invalid date format '{new_due_date}'. Please use YYYY-MM-DD (e.g., 2025-12-31) or ISO datetime format.")
            new_due_date = get_user_input(f"New due date (current: '{task.due_date}'): ")
            if new_due_date == "":  # User pressed Enter to keep current value
                new_due_date = None
                break
    elif new_due_date == "":  # User pressed Enter to keep current value
        new_due_date = None

    try:
        result = task_manager.update_task(
            task_id,
            title=new_title,
            description=new_description,
            priority=new_priority,
            tags=new_tags,
            due_date=new_due_date
        )
        if result:
            print("Task updated successfully.")
        else:
            print("Failed to update task.")
    except ValueError as e:
        print(f"Error updating task: {e}")


def delete_existing_task(task_manager: TaskManager):
    """Delete an existing task."""
    print("\n--- Delete Task ---")
    task_id = get_valid_task_id(task_manager, "Enter task ID or display number to delete: ")
    if not task_id:
        return

    # Use the enhanced delete method with feedback
    task_manager.delete_task_with_feedback(task_id)


def mark_task_complete(task_manager: TaskManager):
    """Mark a task as complete."""
    print("\n--- Mark Task Complete ---")
    task_id = get_valid_task_id(task_manager, "Enter task ID or display number to mark as complete: ")
    if not task_id:
        return

    result = task_manager.mark_task_status(task_id, "complete")
    if result:
        print("Task marked as complete successfully.")
    else:
        print(f"Failed to mark task as complete. Task with ID '{task_id}' not found.")
        # Show available tasks
        all_tasks = task_manager.view_tasks()
        if all_tasks:
            print("\nAvailable tasks:")
            display_tasks(all_tasks)


def mark_task_incomplete(task_manager: TaskManager):
    """Mark a task as incomplete."""
    print("\n--- Mark Task Incomplete ---")
    task_id = get_valid_task_id(task_manager, "Enter task ID or display number to mark as incomplete: ")
    if not task_id:
        return

    result = task_manager.mark_task_status(task_id, "incomplete")
    if result:
        print("Task marked as incomplete successfully.")
    else:
        print(f"Failed to mark task as incomplete. Task with ID '{task_id}' not found.")
        # Show available tasks
        all_tasks = task_manager.view_tasks()
        if all_tasks:
            print("\nAvailable tasks:")
            display_tasks(all_tasks)


def view_tasks_by_status(task_manager: TaskManager):
    """View tasks by status."""
    print("\n--- View Tasks by Status ---")
    print("1. Incomplete tasks")
    print("2. Complete tasks")
    print("3. All tasks")

    choice = get_user_input("Select option (1-3): ")

    if choice == "1":
        status = "incomplete"
    elif choice == "2":
        status = "complete"
    elif choice == "3":
        status = "all"
    else:
        print("Invalid choice. Showing all tasks.")
        status = "all"

    tasks = task_manager.view_tasks(status=status)
    if not tasks:
        print(f"No {status.lower()} tasks found.")
    else:
        print(f"\n--- {status.title()} Tasks ---")
        display_tasks(tasks)


def view_tasks_by_priority(task_manager: TaskManager):
    """View tasks by priority."""
    print("\n--- View Tasks by Priority ---")
    print("1. High priority")
    print("2. Medium priority")
    print("3. Low priority")
    print("4. All priorities")

    choice = get_user_input("Select option (1-4): ")

    if choice == "1":
        priority = "high"
    elif choice == "2":
        priority = "medium"
    elif choice == "3":
        priority = "low"
    elif choice == "4":
        priority = None
    else:
        print("Invalid choice. Showing all priorities.")
        priority = None

    if priority:
        tasks = task_manager.view_tasks(priority=priority)
        print(f"\n--- {priority.title()} Priority Tasks ---")
    else:
        tasks = task_manager.view_tasks()
        print(f"\n--- All Priority Tasks ---")

    if not tasks:
        print("No tasks found.")
    else:
        display_tasks(tasks)


def search_tasks(task_manager: TaskManager):
    """Search tasks by keyword."""
    print("\n--- Search Tasks ---")
    keyword = get_user_input("Enter keyword to search: ")

    if not keyword:
        print("No keyword provided. Showing all tasks.")
        tasks = task_manager.view_tasks()
    else:
        # Use the proper search functionality from TaskManager
        tasks = task_manager.search_tasks(keyword)

    if not tasks:
        print("No tasks found matching your search.")
    else:
        print(f"\n--- Search Results for '{keyword}' ---")
        display_tasks(tasks)


def update_task_priority(task_manager: TaskManager):
    """Update task priority."""
    print("\n--- Update Task Priority ---")
    task_id = get_valid_task_id(task_manager, "Enter task ID or display number: ")
    if not task_id:
        return

    # Check if task exists
    task = task_manager.get_task(task_id)
    if not task:
        print(f"Task with ID '{task_id}' not found.")
        return

    print(f"Current priority for '{task.title}': {task.priority.name.title()}")
    print("Select new priority:")
    print("1. High")
    print("2. Medium")
    print("3. Low")

    choice = get_user_input("Enter choice (1-3): ")
    priority_map = {"1": "high", "2": "medium", "3": "low"}
    new_priority = priority_map.get(choice)

    if not new_priority:
        print("Invalid choice. Priority not updated.")
        return

    result = task_manager.update_task_priority(task_id, new_priority)
    if result:
        print(f"Task priority updated to {new_priority}.")
    else:
        print("Failed to update task priority.")


def update_task_tags(task_manager: TaskManager):
    """Update task tags completely."""
    print("\n--- Update Task Tags ---")
    task_id = get_valid_task_id(task_manager, "Enter task ID or display number: ")
    if not task_id:
        return

    # Check if task exists
    task = task_manager.get_task(task_id)
    if not task:
        print(f"Task with ID '{task_id}' not found.")
        return

    print(f"Current tags for '{task.title}': {', '.join(task.tags) if task.tags else 'None'}")
    new_tags_input = get_user_input("Enter new tags separated by commas (or press Enter to clear): ")

    if new_tags_input:
        new_tags = [tag.strip() for tag in new_tags_input.split(",") if tag.strip()]
    else:
        new_tags = []

    result = task_manager.update_task_tags(task_id, new_tags)
    if result:
        print("Task tags updated successfully.")
    else:
        print("Failed to update task tags.")


def add_tag_to_task(task_manager: TaskManager):
    """Add a single tag to a task."""
    print("\n--- Add Tag to Task ---")
    task_id = get_valid_task_id(task_manager, "Enter task ID or display number: ")
    if not task_id:
        return

    # Check if task exists
    task = task_manager.get_task(task_id)
    if not task:
        print(f"Task with ID '{task_id}' not found.")
        return

    print(f"Current tags for '{task.title}': {', '.join(task.tags) if task.tags else 'None'}")
    tag_to_add = get_user_input("Enter tag to add: ")

    if not tag_to_add:
        print("No tag provided. Nothing to add.")
        return

    result = task_manager.add_tag_to_task(task_id, tag_to_add)
    if result:
        print(f"Tag '{tag_to_add}' added to task successfully.")
    else:
        print("Failed to add tag to task.")


def remove_tag_from_task(task_manager: TaskManager):
    """Remove a single tag from a task."""
    print("\n--- Remove Tag from Task ---")
    task_id = get_valid_task_id(task_manager, "Enter task ID or display number: ")
    if not task_id:
        return

    # Check if task exists
    task = task_manager.get_task(task_id)
    if not task:
        print(f"Task with ID '{task_id}' not found.")
        return

    if not task.tags:
        print(f"Task '{task.title}' has no tags to remove.")
        return

    print(f"Current tags for '{task.title}': {', '.join(task.tags)}")
    tag_to_remove = get_user_input("Enter tag to remove: ")

    if not tag_to_remove:
        print("No tag provided. Nothing to remove.")
        return

    result = task_manager.remove_tag_from_task(task_id, tag_to_remove)
    if result:
        print(f"Tag '{tag_to_remove}' removed from task successfully.")
    else:
        print("Failed to remove tag from task.")


def filter_tasks_menu(task_manager: TaskManager):
    """Filter tasks by various criteria."""
    print("\n--- Filter Tasks ---")

    filters = {}

    # Ask for status filter
    print("Filter by status:")
    print("1. All tasks")
    print("2. Incomplete tasks")
    print("3. Complete tasks")
    status_choice = get_user_input("Select status filter (1-3, Enter to skip): ")
    if status_choice == "2":
        filters['status'] = 'incomplete'
    elif status_choice == "3":
        filters['status'] = 'complete'

    # Ask for priority filter
    print("\nFilter by priority:")
    print("1. All priorities")
    print("2. High priority")
    print("3. Medium priority")
    print("4. Low priority")
    priority_choice = get_user_input("Select priority filter (1-4, Enter to skip): ")
    if priority_choice == "2":
        filters['priority'] = 'high'
    elif priority_choice == "3":
        filters['priority'] = 'medium'
    elif priority_choice == "4":
        filters['priority'] = 'low'

    # Ask for tag filter
    tag_filter = get_user_input("\nEnter tag to filter by (Enter to skip): ")
    if tag_filter:
        filters['tags'] = [tag_filter]

    # Get filtered tasks
    filtered_tasks = task_manager.filter_tasks(filters)

    if not filtered_tasks:
        print("No tasks match your filters.")
    else:
        print(f"\n--- Filtered Tasks ({len(filtered_tasks)} found) ---")
        display_tasks(filtered_tasks)


def sort_tasks_menu(task_manager: TaskManager):
    """Sort tasks by various criteria."""
    print("\n--- Sort Tasks ---")

    print("Sort by:")
    print("1. Priority (High → Medium → Low)")
    print("2. Due Date")
    print("3. Alphabetically")

    sort_choice = get_user_input("Select sort option (1-3): ")

    if sort_choice == "1":
        sort_by = 'priority'
    elif sort_choice == "2":
        sort_by = 'due_date'
    elif sort_choice == "3":
        sort_by = 'alphabetical'
    else:
        print("Invalid choice. Defaulting to priority sort.")
        sort_by = 'priority'

    # Ask if user wants to filter before sorting
    filter_before_sort = get_user_input("Do you want to filter tasks first? (y/n): ").lower()

    filters = None
    if filter_before_sort == 'y':
        filters = {}

        # Ask for status filter
        print("\nFilter by status:")
        print("1. All tasks")
        print("2. Incomplete tasks")
        print("3. Complete tasks")
        status_choice = get_user_input("Select status filter (1-3, Enter to skip): ")
        if status_choice == "2":
            filters['status'] = 'incomplete'
        elif status_choice == "3":
            filters['status'] = 'complete'

        # Ask for priority filter
        print("\nFilter by priority:")
        print("1. All priorities")
        print("2. High priority")
        print("3. Medium priority")
        print("4. Low priority")
        priority_choice = get_user_input("Select priority filter (1-4, Enter to skip): ")
        if priority_choice == "2":
            filters['priority'] = 'high'
        elif priority_choice == "3":
            filters['priority'] = 'medium'
        elif priority_choice == "4":
            filters['priority'] = 'low'

    # Get sorted tasks
    if filters:
        sorted_tasks = task_manager.get_sorted_tasks(sort_by, filters)
    else:
        all_tasks = task_manager.view_tasks()
        sorted_tasks = task_manager.sort_tasks(all_tasks, sort_by)

    if not sorted_tasks:
        print("No tasks to display.")
    else:
        print(f"\n--- Sorted Tasks ({len(sorted_tasks)} total) ---")
        display_tasks(sorted_tasks)


def add_recurring_task(task_manager: TaskManager):
    """Add a recurring task."""
    print("\n--- Add Recurring Task ---")

    # Get task details from user
    title, description, priority, tags, due_date = get_task_details_from_user()

    # Get recurrence rule
    print("\nSelect recurrence rule:")
    print("1. Daily")
    print("2. Weekly")
    print("3. Monthly")
    print("4. Yearly")

    recurrence_choice = get_user_input("Enter choice (1-4): ")
    recurrence_map = {"1": "daily", "2": "weekly", "3": "monthly", "4": "yearly"}
    recurrence_rule = recurrence_map.get(recurrence_choice, "daily")

    # Get next occurrence
    next_occurrence = get_user_input("Enter next occurrence (YYYY-MM-DD or ISO format): ")
    if next_occurrence and not validate_iso_datetime(next_occurrence):
        print(f"Error: Invalid date format '{next_occurrence}'. Please use YYYY-MM-DD (e.g., 2025-12-31) or ISO datetime format.")
        next_occurrence = get_user_input("Enter next occurrence (YYYY-MM-DD or ISO format): ")

    # Get end date (optional)
    end_date = get_user_input("Enter end date (YYYY-MM-DD or ISO format, optional): ")
    if end_date and not validate_iso_datetime(end_date):
        print(f"Error: Invalid date format '{end_date}'. Please use YYYY-MM-DD (e.g., 2025-12-31) or ISO datetime format.")
        end_date = get_user_input("Enter end date (YYYY-MM-DD or ISO format, optional): ")
    if not end_date:
        end_date = None

    # Get continuation policy
    print("\nSelect continuation policy after completion:")
    print("1. Always continue")
    print("2. Prompt user")
    print("3. Stop if completed")

    continue_choice = get_user_input("Enter choice (1-3): ")
    continue_map = {"1": "always_continue", "2": "prompt_user", "3": "stop_if_completed"}
    continue_policy = continue_map.get(continue_choice, "always_continue")

    try:
        # Create recurring task using the command function
        from cli.commands import create_recurring_task_from_user_input, add_recurring_task_to_storage
        recurring_task = create_recurring_task_from_user_input(
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date,
            recurrence_rule=recurrence_rule,
            next_occurrence=next_occurrence,
            end_date=end_date,
            continue_after_completion=continue_policy
        )

        if recurring_task:
            # In a complete implementation, we would save this to persistent storage
            add_recurring_task_to_storage(recurring_task)
            print(f"\nRecurring task '{recurring_task.base_task.title}' added successfully!")
            print(f"Recurrence rule: {recurring_task.recurrence_rule.value}")
            print(f"Next occurrence: {recurring_task.next_occurrence}")
        else:
            print("Failed to create recurring task.")
    except Exception as e:
        print(f"Error creating recurring task: {e}")


def add_reminder(task_manager: TaskManager):
    """Add a reminder for a task."""
    print("\n--- Add Reminder ---")

    # Get task ID
    task_id = get_valid_task_id(task_manager, "Enter task ID or display number to add reminder for: ")
    if not task_id:
        return

    # Get reminder time
    reminder_time = get_user_input("Enter reminder time (YYYY-MM-DD or ISO format): ")
    if not validate_iso_datetime(reminder_time):
        print(f"Error: Invalid date format '{reminder_time}'. Please use YYYY-MM-DD (e.g., 2025-12-31) or ISO datetime format.")
        reminder_time = get_user_input("Enter reminder time (YYYY-MM-DD or ISO format): ")

    try:
        # Create reminder using the command function
        from cli.commands import create_reminder_from_user_input, add_reminder_to_storage
        reminder = create_reminder_from_user_input(task_id, reminder_time)

        if reminder:
            # In a complete implementation, we would save this to persistent storage
            add_reminder_to_storage(reminder)
            print(f"\nReminder added successfully for task {task_id}!")
            print(f"Reminder time: {reminder.reminder_time}")
            print(f"Status: {reminder.status}")
        else:
            print("Failed to create reminder.")
    except Exception as e:
        print(f"Error creating reminder: {e}")


def list_recurring_tasks():
    """List all recurring tasks."""
    print("\n--- Recurring Tasks ---")
    from cli.commands import list_recurring_tasks as get_recurring_tasks
    recurring_tasks = get_recurring_tasks()

    if not recurring_tasks:
        print("No recurring tasks found.")
    else:
        for i, rt in enumerate(recurring_tasks, 1):
            status = "Active" if rt.is_active else "Inactive"
            print(f"{i}. {rt.base_task.title} - {rt.recurrence_rule.value} - Next: {rt.next_occurrence} - {status}")
        print(f"\nTotal recurring tasks: {len(recurring_tasks)}")


def list_reminders():
    """List all reminders."""
    print("\n--- Reminders ---")
    from cli.commands import list_reminders as get_reminders
    reminders = get_reminders()

    if not reminders:
        print("No reminders found.")
    else:
        for i, r in enumerate(reminders, 1):
            print(f"{i}. Task {r.task_id} - {r.reminder_time} - Status: {r.status}")
        print(f"\nTotal reminders: {len(reminders)}")


if __name__ == "__main__":
    run_menu()