import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.database import get_session
from backend.main import app  # Adjust import based on your main app location
from backend.models import User, Task
from backend.config import settings

# Database setup for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency
def override_get_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)

class TestAPITemplate:
    """
    Template for API endpoint testing with comprehensive test cases
    """

    def setup_method(self):
        """
        Setup method to initialize test data
        """
        self.db = TestingSessionLocal()

        # Create test user
        test_user = User(
            email="test@example.com",
            # Add other required fields based on your User model
        )
        self.db.add(test_user)
        self.db.commit()
        self.db.refresh(test_user)
        self.test_user = test_user

        # Create test task
        test_task = Task(
            title="Test Task",
            description="Test Description",
            user_id=test_user.id,
            # Add other required fields based on your Task model
        )
        self.db.add(test_task)
        self.db.commit()
        self.db.refresh(test_task)
        self.test_task = test_task

    def teardown_method(self):
        """
        Teardown method to clean up test data
        """
        self.db.query(Task).delete()
        self.db.query(User).delete()
        self.db.commit()
        self.db.close()

    def test_get_tasks_authenticated(self):
        """
        Test getting tasks with valid authentication
        """
        response = client.get(
            f"/api/{self.test_user.id}/tasks",
            headers={"Authorization": f"Bearer {self.get_auth_token()}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_tasks_unauthorized(self):
        """
        Test getting tasks without authentication
        """
        response = client.get(f"/api/{self.test_user.id}/tasks")
        assert response.status_code == 401

    def test_create_task_authenticated(self):
        """
        Test creating task with valid authentication
        """
        task_data = {
            "title": "New Task",
            "description": "New Description",
            "status": "incomplete"
        }
        response = client.post(
            f"/api/{self.test_user.id}/tasks",
            json=task_data,
            headers={"Authorization": f"Bearer {self.get_auth_token()}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == task_data["title"]

    def test_create_task_invalid_data(self):
        """
        Test creating task with invalid data
        """
        invalid_task_data = {
            "title": "",  # Empty title should fail validation
            "description": "Valid description"
        }
        response = client.post(
            f"/api/{self.test_user.id}/tasks",
            json=invalid_task_data,
            headers={"Authorization": f"Bearer {self.get_auth_token()}"}
        )
        assert response.status_code == 422

    def test_update_task(self):
        """
        Test updating an existing task
        """
        update_data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "status": "complete"
        }
        response = client.put(
            f"/api/{self.test_user.id}/tasks/{self.test_task.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {self.get_auth_token()}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]

    def test_delete_task(self):
        """
        Test deleting a task
        """
        response = client.delete(
            f"/api/{self.test_user.id}/tasks/{self.test_task.id}",
            headers={"Authorization": f"Bearer {self.get_auth_token()}"}
        )
        assert response.status_code == 200

    def get_auth_token(self):
        """
        Helper method to get authentication token for testing
        """
        # In real implementation, you might need to sign in or generate a test token
        # This is a placeholder - implement based on your auth system
        return "test_token_placeholder"