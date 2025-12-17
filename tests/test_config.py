"""
Tests for the configuration management system.
"""
import json
import tempfile
from pathlib import Path
from src.utils.config import Config


def test_config_creation():
    """Test that configuration is created with default values."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config = Config(config_dir=temp_dir)

        # Check that default values exist
        assert config.get("default_priority") == "medium"
        assert config.get("show_completed") is True
        assert config.get("auto_backup") is True


def test_config_set_get():
    """Test setting and getting configuration values."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config = Config(config_dir=temp_dir)

        # Set a value
        config.set("test_key", "test_value")

        # Get the value back
        assert config.get("test_key") == "test_value"


def test_config_persistence():
    """Test that configuration changes are persisted to file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir)

        # Create config and set a value
        config1 = Config(config_dir=temp_dir)
        config1.set("persistent_key", "persistent_value")

        # Create another config instance and check the value is still there
        config2 = Config(config_dir=temp_dir)
        assert config2.get("persistent_key") == "persistent_value"

        # Verify the file was created and contains the value
        config_file = config_path / "config.json"
        assert config_file.exists()

        with open(config_file, 'r') as f:
            data = json.load(f)
        assert data["persistent_key"] == "persistent_value"


def test_config_update_multiple():
    """Test updating multiple configuration values at once."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config = Config(config_dir=temp_dir)

        updates = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        }

        config.update(updates)

        assert config.get("key1") == "value1"
        assert config.get("key2") == "value2"
        assert config.get("key3") == "value3"


def test_config_defaults():
    """Test that default configuration values are properly set."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config = Config(config_dir=temp_dir)

        # Check all default keys exist
        defaults = {
            "storage_path": str(Path(temp_dir) / "tasks.json"),
            "default_priority": "medium",
            "show_completed": True,
            "auto_backup": True,
            "backup_retention_days": 30
        }

        for key, expected_value in defaults.items():
            assert config.get(key) == expected_value