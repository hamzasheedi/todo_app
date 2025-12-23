import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.services.task_service import TaskService
from backend.models import Task
from backend.schemas import TaskCreate, TaskUpdate
from sqlmodel import Session
from datetime import datetime

class TestTaskService:
    """
    Comprehensive unit test template for TaskService
    """

    @pytest.fixture
    def mock_db_session(self):
        """
        Mock database session fixture
        """
        session = Mock(spec=Session)
        return session

    @pytest.fixture
    def task_service(self, mock_db_session):
        """
        TaskService instance fixture
        """
        return TaskService(db_session=mock_db_session)

    def test_create_task_success(self, task_service, mock_db_session):
        """
        Test successful task creation
        """
        # Arrange
        user_id = "test-user-id"
        task_data = TaskCreate(
            title="Test Task",
            description="Test Description",
            status="incomplete"
        )

        # Mock the database operations
        mock_task = Task(
            id="test-task-id",
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            user_id=user_id,
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )
        mock_db_session.add.return_value = None
        mock_db_session.commit.return_value = None
        mock_db_session.refresh.return_value = None
        type(mock_db_session).exec = Mock(return_value=Mock(first=Mock(return_value=mock_task)))

        # Act
        result = task_service.create_task(user_id, task_data)

        # Assert
        assert result.title == task_data.title
        assert result.description == task_data.description
        assert result.status == task_data.status
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

    def test_create_task_invalid_title(self, task_service):
        """
        Test task creation with invalid title
        """
        # Arrange
        user_id = "test-user-id"
        task_data = TaskCreate(
            title="",  # Invalid: empty title
            description="Test Description",
            status="incomplete"
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Task title is required"):
            task_service.create_task(user_id, task_data)

    def test_get_task_success(self, task_service, mock_db_session):
        """
        Test successful task retrieval
        """
        # Arrange
        user_id = "test-user-id"
        task_id = "test-task-id"
        mock_task = Task(
            id=task_id,
            title="Test Task",
            description="Test Description",
            status="incomplete",
            user_id=user_id,
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )

        mock_statement = Mock()
        mock_db_session.exec.return_value = Mock(first=Mock(return_value=mock_task))

        # Act
        result = task_service.get_task(task_id, user_id)

        # Assert
        assert result.id == task_id
        assert result.title == "Test Task"

    def test_get_task_not_found(self, task_service, mock_db_session):
        """
        Test task retrieval when task doesn't exist
        """
        # Arrange
        user_id = "test-user-id"
        task_id = "non-existent-task-id"
        mock_db_session.exec.return_value = Mock(first=Mock(return_value=None))

        # Act & Assert
        with pytest.raises(Exception):  # Adjust based on your error handling
            task_service.get_task(task_id, user_id)

    def test_update_task_success(self, task_service, mock_db_session):
        """
        Test successful task update
        """
        # Arrange
        user_id = "test-user-id"
        task_id = "test-task-id"
        existing_task = Task(
            id=task_id,
            title="Old Title",
            description="Old Description",
            status="incomplete",
            user_id=user_id,
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )
        update_data = TaskUpdate(
            title="New Title",
            description="New Description",
            status="complete"
        )

        mock_db_session.exec.return_value = Mock(first=Mock(return_value=existing_task))

        # Act
        result = task_service.update_task(task_id, user_id, update_data)

        # Assert
        assert result.title == update_data.title
        assert result.description == update_data.description
        assert result.status == update_data.status
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

    def test_delete_task_success(self, task_service, mock_db_session):
        """
        Test successful task deletion
        """
        # Arrange
        user_id = "test-user-id"
        task_id = "test-task-id"
        mock_task = Task(
            id=task_id,
            title="Test Task",
            description="Test Description",
            status="incomplete",
            user_id=user_id,
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )

        mock_db_session.exec.return_value = Mock(first=Mock(return_value=mock_task))

        # Act
        result = task_service.delete_task(task_id, user_id)

        # Assert
        assert result is True
        mock_db_session.delete.assert_called_once_with(mock_task)
        mock_db_session.commit.assert_called_once()

    def test_get_task_statistics(self, task_service, mock_db_session):
        """
        Test task statistics calculation
        """
        # Arrange
        user_id = "test-user-id"
        tasks = [
            Task(id="1", title="Task 1", status="complete", user_id=user_id, created_date=datetime.utcnow(), updated_date=datetime.utcnow()),
            Task(id="2", title="Task 2", status="incomplete", user_id=user_id, created_date=datetime.utcnow(), updated_date=datetime.utcnow()),
            Task(id="3", title="Task 3", status="complete", user_id=user_id, created_date=datetime.utcnow(), updated_date=datetime.utcnow()),
        ]

        mock_db_session.exec.return_value = Mock(all=Mock(return_value=tasks))

        # Act
        stats = task_service.get_task_statistics(user_id)

        # Assert
        assert stats["total_tasks"] == 3
        assert stats["completed_tasks"] == 2
        assert stats["incomplete_tasks"] == 1
        assert stats["completion_rate"] == 2/3


class TestValidationUtils:
    """
    Unit tests for validation utilities
    """

    def test_validate_email_valid(self):
        """
        Test email validation with valid email
        """
        from backend.utils.validation import ValidationUtils
        result = ValidationUtils.validate_email("test@example.com")
        assert result is True

    def test_validate_email_invalid(self):
        """
        Test email validation with invalid email
        """
        from backend.utils.validation import ValidationUtils
        result = ValidationUtils.validate_email("invalid-email")
        assert result is False

    def test_validate_task_title_valid(self):
        """
        Test task title validation with valid title
        """
        from backend.utils.validation import ValidationUtils
        result = ValidationUtils.validate_task_title("Valid Task Title")
        assert result["is_valid"] is True

    def test_validate_task_title_invalid(self):
        """
        Test task title validation with invalid title
        """
        from backend.utils.validation import ValidationUtils
        result = ValidationUtils.validate_task_title("")  # Empty title
        assert result["is_valid"] is False
        assert len(result["errors"]) > 0


if __name__ == "__main__":
    pytest.main([__file__])