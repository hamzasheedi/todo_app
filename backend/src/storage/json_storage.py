"""
JSON storage manager for the Todo CLI application.

This module provides functionality to save and load tasks to/from JSON files.
"""
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from core.task import Task


class JSONStorage:
    """
    JSON-based storage manager for tasks.

    Handles serialization and deserialization of tasks to/from JSON files.
    """

    def __init__(self, file_path: str = None):
        """
        Initialize the JSON storage manager.

        Args:
            file_path: Path to the JSON file for storage. If not provided,
                      uses the path from the global configuration.
        """
        from utils.config import get_config
        config = get_config()

        if file_path:
            self.file_path = Path(file_path)
        else:
            # Use the storage path from configuration
            storage_path = config.get("storage_path")
            self.file_path = Path(storage_path) if storage_path else Path.home() / ".todo" / "tasks.json"

        # Ensure the directory exists
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            raise PermissionError(f"Cannot create directory for storage file {self.file_path}: {e}")
        except OSError as e:
            raise OSError(f"Cannot create directory for storage file {self.file_path}: {e}")

    def save_tasks(self, tasks: List[Task]) -> None:
        """
        Save a list of tasks to the JSON file.

        Args:
            tasks: List of Task objects to save

        Raises:
            IOError: If there's an error writing to the file
        """
        try:
            # Convert tasks to dictionary representation
            tasks_data = [task.to_dict() for task in tasks]

            # Write to file
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, indent=2, ensure_ascii=False)

        except IOError as e:
            raise IOError(f"Failed to save tasks to {self.file_path}: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error while saving tasks: {e}")

    def load_tasks(self) -> List[Task]:
        """
        Load tasks from the JSON file.

        Returns:
            List of Task objects loaded from the file

        Raises:
            IOError: If there's an error reading from the file
            ValueError: If the file contains invalid data
        """
        if not self.file_path.exists():
            # Return empty list if file doesn't exist
            return []

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
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
                    raise ValueError(f"Invalid task data format in {self.file_path}: {e}")

            return tasks

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {self.file_path}: {e}")
        except IOError as e:
            raise IOError(f"Failed to load tasks from {self.file_path}: {e}")
        except ValueError:
            # Re-raise ValueError as-is since it's already properly formatted
            raise
        except Exception as e:
            raise Exception(f"Unexpected error while loading tasks: {e}")

    def add_task(self, task: Task) -> None:
        """
        Add a single task to storage.

        Args:
            task: Task object to add

        Raises:
            IOError: If there's an error writing to the file
        """
        tasks = self.load_tasks()
        tasks.append(task)
        self.save_tasks(tasks)

    def update_task(self, task_id: str, updated_task: Task) -> bool:
        """
        Update a task in storage.

        Args:
            task_id: ID of the task to update
            updated_task: Updated Task object

        Returns:
            True if the task was found and updated, False otherwise
        """
        tasks = self.load_tasks()
        for i, task in enumerate(tasks):
            if task.id == task_id:
                tasks[i] = updated_task
                self.save_tasks(tasks)
                return True
        return False

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task from storage.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if the task was found and deleted, False otherwise
        """
        tasks = self.load_tasks()
        for i, task in enumerate(tasks):
            if task.id == task_id:
                del tasks[i]
                self.save_tasks(tasks)
                return True
        return False

    def task_exists(self, task_id: str) -> bool:
        """
        Check if a task exists in storage.

        Args:
            task_id: ID of the task to check

        Returns:
            True if the task exists, False otherwise
        """
        tasks = self.load_tasks()
        return any(task.id == task_id for task in tasks)

    def clear_all_tasks(self) -> None:
        """
        Clear all tasks from storage.
        """
        self.save_tasks([])

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a specific task by ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task object if found, None otherwise
        """
        tasks = self.load_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None