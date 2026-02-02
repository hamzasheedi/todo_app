"""
Backup and restore functionality for the Todo CLI application.

This module provides backup and restore capabilities for task data.
"""
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional
from storage.json_storage import JSONStorage
from utils.config import get_config


class BackupManager:
    """
    Manager class for handling backup and restore operations.
    """

    def __init__(self):
        """Initialize the backup manager with configuration."""
        config = get_config()
        storage_path = config.get("storage_path")
        self.storage_path = Path(storage_path) if storage_path else Path.home() / ".todo" / "tasks.json"

        # Set backup directory based on config
        backup_dir = config.get("backup_location", str(Path.home() / "Documents" / "todo-backups"))
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, backup_name: Optional[str] = None) -> str:
        """
        Create a backup of the current task data.

        Args:
            backup_name: Optional name for the backup file. If not provided,
                        a timestamp-based name will be generated.

        Returns:
            Path to the created backup file.
        """
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"tasks_backup_{timestamp}.json"

        backup_path = self.backup_dir / backup_name

        # Copy the current tasks file to the backup location
        if self.storage_path.exists():
            shutil.copy2(self.storage_path, backup_path)
        else:
            # If there's no tasks file, create an empty backup
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

        return str(backup_path)

    def list_backups(self) -> list[str]:
        """
        List all available backup files.

        Returns:
            List of backup file paths.
        """
        backups = []
        for file_path in self.backup_dir.glob("tasks_backup_*.json"):
            backups.append(str(file_path))

        # Sort by modification time, newest first
        backups.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return backups

    def restore_from_backup(self, backup_path: str) -> bool:
        """
        Restore task data from a backup file.

        Args:
            backup_path: Path to the backup file to restore from.

        Returns:
            True if the restore was successful, False otherwise.
        """
        backup_file = Path(backup_path)

        if not backup_file.exists():
            raise FileNotFoundError(f"Backup file does not exist: {backup_path}")

        try:
            # Validate that the backup file contains valid JSON
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)

            if not isinstance(backup_data, list):
                raise ValueError("Invalid backup file format: expected a list of tasks")

            # Copy the backup file to the main storage location
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup_file, self.storage_path)

            return True
        except (json.JSONDecodeError, ValueError, IOError) as e:
            raise Exception(f"Failed to restore from backup: {e}")

    def delete_backup(self, backup_path: str) -> bool:
        """
        Delete a backup file.

        Args:
            backup_path: Path to the backup file to delete.

        Returns:
            True if the deletion was successful, False otherwise.
        """
        backup_file = Path(backup_path)

        if backup_file.exists():
            backup_file.unlink()
            return True

        return False

    def cleanup_old_backups(self, retention_days: int = 30) -> int:
        """
        Delete backup files older than the specified number of days.

        Args:
            retention_days: Number of days to keep backups (default: 30).

        Returns:
            Number of deleted backup files.
        """
        from datetime import timedelta

        cutoff_date = datetime.now() - timedelta(days=retention_days)
        deleted_count = 0

        for backup_file in self.backup_dir.glob("tasks_backup_*.json"):
            if datetime.fromtimestamp(backup_file.stat().st_mtime) < cutoff_date:
                backup_file.unlink()
                deleted_count += 1

        return deleted_count


def get_backup_manager() -> BackupManager:
    """
    Get the global backup manager instance.

    Returns:
        BackupManager instance
    """
    return BackupManager()


def create_backup(backup_name: Optional[str] = None) -> str:
    """
    Create a backup of the current task data.

    Args:
        backup_name: Optional name for the backup file.

    Returns:
        Path to the created backup file.
    """
    backup_manager = get_backup_manager()
    return backup_manager.create_backup(backup_name)


def list_backups() -> list[str]:
    """
    List all available backup files.

    Returns:
        List of backup file paths.
    """
    backup_manager = get_backup_manager()
    return backup_manager.list_backups()


def restore_from_backup(backup_path: str) -> bool:
    """
    Restore task data from a backup file.

    Args:
        backup_path: Path to the backup file to restore from.

    Returns:
        True if the restore was successful, False otherwise.
    """
    backup_manager = get_backup_manager()
    return backup_manager.restore_from_backup(backup_path)


def delete_backup(backup_path: str) -> bool:
    """
    Delete a backup file.

    Args:
        backup_path: Path to the backup file to delete.

    Returns:
        True if the deletion was successful, False otherwise.
    """
    backup_manager = get_backup_manager()
    return backup_manager.delete_backup(backup_path)


def cleanup_old_backups(retention_days: int = 30) -> int:
    """
    Delete backup files older than the specified number of days.

    Args:
        retention_days: Number of days to keep backups (default: 30).

    Returns:
        Number of deleted backup files.
    """
    backup_manager = get_backup_manager()
    return backup_manager.cleanup_old_backups(retention_days)