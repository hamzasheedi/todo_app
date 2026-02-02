"""
Configuration management for the Todo CLI application.

This module handles application configuration, storing settings in ~/.todo/config.json.
"""
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Configuration manager for the Todo CLI application."""

    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize the configuration manager.

        Args:
            config_dir: Optional custom config directory path. If not provided,
                       uses ~/.todo as the default location.
        """
        if config_dir:
            self.config_path = Path(config_dir)
        else:
            home_dir = Path.home()
            self.config_path = home_dir / ".todo"

        self.config_file = self.config_path / "config.json"
        self._ensure_config_directory()
        self._default_config = {
            "storage_path": str(self.config_path / "tasks.json"),
            "default_priority": "medium",
            "show_completed": True,
            "auto_backup": True,
            "backup_retention_days": 30
        }
        self._config = self._load_config()

    def _ensure_config_directory(self) -> None:
        """Ensure the configuration directory exists."""
        self.config_path.mkdir(parents=True, exist_ok=True)

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file, creating default if it doesn't exist.

        Returns:
            Dictionary containing configuration values.
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Merge with defaults to ensure all keys exist
                for key, value in self._default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            except (json.JSONDecodeError, IOError):
                # If there's an error loading the config, return defaults
                return self._default_config.copy()
        else:
            # Create config with default values
            config = self._default_config.copy()
            self._save_config(config)
            return config

    def _save_config(self, config: Dict[str, Any]) -> None:
        """
        Save configuration to file.

        Args:
            config: Dictionary containing configuration values to save.
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise IOError(f"Failed to save configuration to {self.config_file}: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key to retrieve.
            default: Default value to return if key doesn't exist.

        Returns:
            Configuration value or default if not found.
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            key: Configuration key to set.
            value: Value to set for the key.
        """
        self._config[key] = value
        self._save_config(self._config)

    def update(self, updates: Dict[str, Any]) -> None:
        """
        Update multiple configuration values at once.

        Args:
            updates: Dictionary of key-value pairs to update.
        """
        self._config.update(updates)
        self._save_config(self._config)

    def reset_to_defaults(self) -> None:
        """Reset all configuration values to their defaults."""
        self._config = self._default_config.copy()
        self._save_config(self._config)


# Global configuration instance
_config_instance: Optional[Config] = None


def get_config() -> Config:
    """
    Get the global configuration instance.

    Returns:
        Config instance for the application.
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance