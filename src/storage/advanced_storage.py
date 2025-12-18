"""
Advanced storage manager for the Todo CLI application.

This module provides functionality to save and load tasks, recurring tasks,
and reminders to/from JSON files.
"""
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from core.task import Task
from core.recurring_task import RecurringTask
from core.reminder import Reminder


class AdvancedJSONStorage:
    """
    Advanced JSON-based storage manager for tasks, recurring tasks, and reminders.

    Handles serialization and deserialization of all entities to/from JSON files.
    """

    def __init__(self, base_dir: str = None):
        """
        Initialize the advanced JSON storage manager.

        Args:
            base_dir: Base directory for storage files. If not provided,
                      uses the default configuration directory.
        """
        from utils.config import get_config
        config = get_config()

        if base_dir:
            self.base_path = Path(base_dir)
        else:
            # Use the storage path from configuration
            storage_path = config.get("storage_path")
            if storage_path:
                self.base_path = Path(storage_path).parent  # Get directory, not file
            else:
                self.base_path = Path.home() / ".todo"

        # Ensure the directory exists
        try:
            self.base_path.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            raise PermissionError(f"Cannot create directory for storage: {e}")
        except OSError as e:
            raise OSError(f"Cannot create directory for storage: {e}")

        # Define file paths
        self.tasks_file = self.base_path / "tasks.json"
        self.recurring_tasks_file = self.base_path / "recurring_tasks.json"
        self.reminders_file = self.base_path / "reminders.json"

    def save_tasks(self, tasks: List[Task]) -> None:
        """
        Save a list of tasks to the JSON file.
        """
        try:
            # Convert tasks to dictionary representation
            tasks_data = [task.to_dict() for task in tasks]

            # Write to file
            with open(self.tasks_file, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, indent=2, ensure_ascii=False)

        except IOError as e:
            raise IOError(f"Failed to save tasks to {self.tasks_file}: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error while saving tasks: {e}")

    def load_tasks(self) -> List[Task]:
        """
        Load tasks from the JSON file.
        """
        if not self.tasks_file.exists():
            # Return empty list if file doesn't exist
            return []

        try:
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)

            if not isinstance(tasks_data, list):
                raise ValueError("Invalid file format: expected a list of tasks")

            # Convert dictionary representations back to Task objects
            tasks = []
            for task_data in tasks_data:
                if not isinstance(task_data, dict):
                    raise ValueError("Invalid task data format")

                try:
                    task = Task.from_dict(task_data)
                    tasks.append(task)
                except (KeyError, ValueError) as e:
                    raise ValueError(f"Invalid task data format in {self.tasks_file}: {e}")

            return tasks

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {self.tasks_file}: {e}")
        except IOError as e:
            raise IOError(f"Failed to load tasks from {self.tasks_file}: {e}")
        except ValueError:
            # Re-raise ValueError as-is since it's already properly formatted
            raise
        except Exception as e:
            raise Exception(f"Unexpected error while loading tasks: {e}")

    def save_recurring_tasks(self, recurring_tasks: List[RecurringTask]) -> None:
        """
        Save a list of recurring tasks to the JSON file.
        """
        try:
            # Convert recurring tasks to dictionary representation
            recurring_tasks_data = [rt.to_dict() for rt in recurring_tasks]

            # Write to file
            with open(self.recurring_tasks_file, 'w', encoding='utf-8') as f:
                json.dump(recurring_tasks_data, f, indent=2, ensure_ascii=False)

        except IOError as e:
            raise IOError(f"Failed to save recurring tasks to {self.recurring_tasks_file}: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error while saving recurring tasks: {e}")

    def load_recurring_tasks(self) -> List[RecurringTask]:
        """
        Load recurring tasks from the JSON file.
        """
        if not self.recurring_tasks_file.exists():
            # Return empty list if file doesn't exist
            return []

        try:
            with open(self.recurring_tasks_file, 'r', encoding='utf-8') as f:
                recurring_tasks_data = json.load(f)

            if not isinstance(recurring_tasks_data, list):
                raise ValueError("Invalid file format: expected a list of recurring tasks")

            # Convert dictionary representations back to RecurringTask objects
            recurring_tasks = []
            for rt_data in recurring_tasks_data:
                if not isinstance(rt_data, dict):
                    raise ValueError("Invalid recurring task data format")

                try:
                    from core.recurring_task import RecurringTask
                    rt = RecurringTask.from_dict(rt_data)
                    recurring_tasks.append(rt)
                except (KeyError, ValueError) as e:
                    raise ValueError(f"Invalid recurring task data format in {self.recurring_tasks_file}: {e}")

            return recurring_tasks

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {self.recurring_tasks_file}: {e}")
        except IOError as e:
            raise IOError(f"Failed to load recurring tasks from {self.recurring_tasks_file}: {e}")
        except ValueError:
            # Re-raise ValueError as-is since it's already properly formatted
            raise
        except Exception as e:
            raise Exception(f"Unexpected error while loading recurring tasks: {e}")

    def save_reminders(self, reminders: List[Reminder]) -> None:
        """
        Save a list of reminders to the JSON file.
        """
        try:
            # Convert reminders to dictionary representation
            reminders_data = [reminder.to_dict() for reminder in reminders]

            # Write to file
            with open(self.reminders_file, 'w', encoding='utf-8') as f:
                json.dump(reminders_data, f, indent=2, ensure_ascii=False)

        except IOError as e:
            raise IOError(f"Failed to save reminders to {self.reminders_file}: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error while saving reminders: {e}")

    def load_reminders(self) -> List[Reminder]:
        """
        Load reminders from the JSON file.
        """
        if not self.reminders_file.exists():
            # Return empty list if file doesn't exist
            return []

        try:
            with open(self.reminders_file, 'r', encoding='utf-8') as f:
                reminders_data = json.load(f)

            if not isinstance(reminders_data, list):
                raise ValueError("Invalid file format: expected a list of reminders")

            # Convert dictionary representations back to Reminder objects
            reminders = []
            for reminder_data in reminders_data:
                if not isinstance(reminder_data, dict):
                    raise ValueError("Invalid reminder data format")

                try:
                    from core.reminder import Reminder
                    reminder = Reminder.from_dict(reminder_data)
                    reminders.append(reminder)
                except (KeyError, ValueError) as e:
                    raise ValueError(f"Invalid reminder data format in {self.reminders_file}: {e}")

            return reminders

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {self.reminders_file}: {e}")
        except IOError as e:
            raise IOError(f"Failed to load reminders from {self.reminders_file}: {e}")
        except ValueError:
            # Re-raise ValueError as-is since it's already properly formatted
            raise
        except Exception as e:
            raise Exception(f"Unexpected error while loading reminders: {e}")

    def add_task(self, task: Task) -> None:
        """
        Add a single task to storage.
        """
        tasks = self.load_tasks()
        tasks.append(task)
        self.save_tasks(tasks)

    def add_recurring_task(self, recurring_task: RecurringTask) -> None:
        """
        Add a single recurring task to storage.
        """
        recurring_tasks = self.load_recurring_tasks()
        recurring_tasks.append(recurring_task)
        self.save_recurring_tasks(recurring_tasks)

    def add_reminder(self, reminder: Reminder) -> None:
        """
        Add a single reminder to storage.
        """
        reminders = self.load_reminders()
        reminders.append(reminder)
        self.save_reminders(reminders)

    def update_task(self, task_id: str, updated_task: Task) -> bool:
        """
        Update a task in storage.
        """
        tasks = self.load_tasks()
        for i, task in enumerate(tasks):
            if task.id == task_id:
                tasks[i] = updated_task
                self.save_tasks(tasks)
                return True
        return False

    def update_recurring_task(self, recurring_task_id: str, updated_recurring_task: RecurringTask) -> bool:
        """
        Update a recurring task in storage.
        """
        recurring_tasks = self.load_recurring_tasks()
        for i, rt in enumerate(recurring_tasks):
            if rt.id == recurring_task_id:
                recurring_tasks[i] = updated_recurring_task
                self.save_recurring_tasks(recurring_tasks)
                return True
        return False

    def update_reminder(self, reminder_id: str, updated_reminder: Reminder) -> bool:
        """
        Update a reminder in storage.
        """
        reminders = self.load_reminders()
        for i, reminder in enumerate(reminders):
            if reminder.id == reminder_id:
                reminders[i] = updated_reminder
                self.save_reminders(reminders)
                return True
        return False

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task from storage.
        """
        tasks = self.load_tasks()
        for i, task in enumerate(tasks):
            if task.id == task_id:
                del tasks[i]
                self.save_tasks(tasks)
                return True
        return False

    def delete_recurring_task(self, recurring_task_id: str) -> bool:
        """
        Delete a recurring task from storage.
        """
        recurring_tasks = self.load_recurring_tasks()
        for i, rt in enumerate(recurring_tasks):
            if rt.id == recurring_task_id:
                del recurring_tasks[i]
                self.save_recurring_tasks(recurring_tasks)
                return True
        return False

    def delete_reminder(self, reminder_id: str) -> bool:
        """
        Delete a reminder from storage.
        """
        reminders = self.load_reminders()
        for i, reminder in enumerate(reminders):
            if reminder.id == reminder_id:
                del reminders[i]
                self.save_reminders(reminders)
                return True
        return False

    def task_exists(self, task_id: str) -> bool:
        """
        Check if a task exists in storage.
        """
        tasks = self.load_tasks()
        return any(task.id == task_id for task in tasks)

    def recurring_task_exists(self, recurring_task_id: str) -> bool:
        """
        Check if a recurring task exists in storage.
        """
        recurring_tasks = self.load_recurring_tasks()
        return any(rt.id == recurring_task_id for rt in recurring_tasks)

    def reminder_exists(self, reminder_id: str) -> bool:
        """
        Check if a reminder exists in storage.
        """
        reminders = self.load_reminders()
        return any(reminder.id == reminder_id for reminder in reminders)

    def clear_all_tasks(self) -> None:
        """
        Clear all tasks from storage.
        """
        self.save_tasks([])

    def clear_all_recurring_tasks(self) -> None:
        """
        Clear all recurring tasks from storage.
        """
        self.save_recurring_tasks([])

    def clear_all_reminders(self) -> None:
        """
        Clear all reminders from storage.
        """
        self.save_reminders([])

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a specific task by ID.
        """
        tasks = self.load_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None

    def get_recurring_task(self, recurring_task_id: str) -> Optional[RecurringTask]:
        """
        Get a specific recurring task by ID.
        """
        recurring_tasks = self.load_recurring_tasks()
        for rt in recurring_tasks:
            if rt.id == recurring_task_id:
                return rt
        return None

    def get_reminder(self, reminder_id: str) -> Optional[Reminder]:
        """
        Get a specific reminder by ID.
        """
        reminders = self.load_reminders()
        for reminder in reminders:
            if reminder.id == reminder_id:
                return reminder
        return None