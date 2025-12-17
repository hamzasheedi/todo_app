"""
Tests for search functionality.
"""
import tempfile
from pathlib import Path
from src.cli.commands import TaskManager


def test_search_functionality():
    """Test search functionality for tasks."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_file = Path(temp_dir) / "test_tasks.json"

        # Create a TaskManager with the temporary storage file
        task_manager = TaskManager()
        from src.storage.json_storage import JSONStorage
        task_manager.storage = JSONStorage(str(storage_file))

        # Add some tasks with different content
        task1 = task_manager.add_task("Buy groceries", description="Milk, bread, eggs")
        task2 = task_manager.add_task("Finish report", description="Complete the quarterly report")
        task3 = task_manager.add_task("Call mom", description="Check on mom's health")
        task4 = task_manager.add_task("Workout", description="Morning exercise routine")

        # Test search in title
        results = task_manager.search_tasks("groceries")
        assert len(results) == 1
        assert results[0].id == task1.id

        # Test search in description
        results = task_manager.search_tasks("milk")
        assert len(results) == 1
        assert results[0].id == task1.id

        # Test search with partial matching
        results = task_manager.search_tasks("report")
        assert len(results) == 1
        assert results[0].id == task2.id

        # Test search with case insensitivity
        results = task_manager.search_tasks("GROCERIES")
        assert len(results) == 1
        assert results[0].id == task1.id

        # Test search with no matches
        results = task_manager.search_tasks("nonexistent")
        assert len(results) == 0

        # Test search that matches multiple tasks
        task5 = task_manager.add_task("More groceries", description="Fruits and vegetables")
        results = task_manager.search_tasks("groceries")
        assert len(results) == 2
        result_ids = {task.id for task in results}
        assert {task1.id, task5.id} == result_ids

        print("All search functionality tests passed!")