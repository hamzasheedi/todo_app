import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool
from unittest.mock import patch, MagicMock
import uuid
from datetime import datetime
import json

from main import app
from models.user import User
from models.task import Task
from database.database import get_session, SessionLocal
from auth.jwt import verify_token, get_current_user
from schemas.user import UserCreate, UserRead
from schemas.task import TaskCreate, TaskRead, TaskUpdate, TaskComplete


# Override the database session for testing
@pytest.fixture(scope="module")
def client():
    """Create a test client with mocked database session"""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def db_session():
    """Create an in-memory database session for each test"""
    engine = create_engine(
        "sqlite:///:memory:",
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session


# Test Suite: Authentication and Authorization

def test_successful_user_registration_and_jwt_token_generation(db_session, client):
    """Test Case 1: Successful User Registration and JWT Token Generation"""
    # Setup: Initialize test database and create test user data
    test_user_id = str(uuid.uuid4())
    test_better_auth_id = "test_auth_12345"
    test_email = "test@example.com"

    # Mock Better Auth JWT token
    mock_jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X2F1dGhfMTIzNDUiLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjk5OTk5OTk5OTl9.test_signature"

    # Mock the JWT verification
    with patch('auth.jwt.verify_token') as mock_verify:
        mock_verify.return_value = {
            "sub": test_better_auth_id,
            "email": test_email,
            "exp": 9999999999  # Far future expiration
        }

        # Send POST request to /api/auth/sync-user with valid JWT and payload
        response = client.post(
            "/api/auth/sync-user",
            headers={"Authorization": f"Bearer {mock_jwt_token}"},
            json={
                "better_auth_id": test_better_auth_id,
                "email": test_email
            }
        )

        # Verify response status code is 200
        assert response.status_code == 200

        # Verify response contains user ID, email, and better_auth_id
        response_data = response.json()
        assert "id" in response_data
        assert response_data["email"] == test_email
        assert response_data["better_auth_id"] == test_better_auth_id


def test_authentication_verification_with_valid_jwt(db_session, client):
    """Test Case 2: Authentication Verification with Valid JWT"""
    # Setup: Create test user in database
    test_user = User(
        email="auth_test@example.com",
        better_auth_id="auth_test_12345"
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    # Mock Better Auth JWT token
    mock_jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdXRoX3Rlc3RfMTIzNDUiLCJlbWFpbCI6ImF1dGhfdGVzdEBleGFtcGxlLmNvbSIsImV4cCI6OTk5OTk5OTk5OX0.test_signature"

    with patch('auth.jwt.verify_token') as mock_verify:
        mock_verify.return_value = {
            "sub": test_user.better_auth_id,
            "email": test_user.email,
            "exp": 9999999999
        }

        # Send GET request to /api/auth/me with valid JWT in Authorization header
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )

        # Verify response status code is 200
        assert response.status_code == 200

        # Verify response contains user ID, email, and better_auth_id
        response_data = response.json()
        assert response_data["id"] == str(test_user.id)
        assert response_data["email"] == test_user.email
        assert response_data["better_auth_id"] == test_user.better_auth_id

        # Verify user ID in response matches the authenticated user
        assert response_data["id"] == str(test_user.id)


def test_unauthorized_access_rejection(client):
    """Test Case 3: Unauthorized Access Rejection"""
    # Setup: Prepare invalid JWT token or omit Authorization header

    # Send GET request to /api/auth/me without JWT token
    response_no_auth = client.get("/api/auth/me")
    # Verify response status code is 401 Unauthorized
    assert response_no_auth.status_code == 401

    # Send GET request to /api/auth/me with invalid JWT token
    response_invalid = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    # Verify response status code is 401 Unauthorized
    assert response_invalid.status_code == 401

    # Send GET request to /api/auth/me with malformed JWT token
    response_malformed = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer malformed.token.format"}
    )
    # Verify response status code is 401 Unauthorized
    assert response_malformed.status_code == 401


def test_successful_task_creation_for_authenticated_user(db_session, client):
    """Test Case 4: Successful Task Creation for Authenticated User"""
    # Setup: Create authenticated user
    test_user = User(
        email="task_test@example.com",
        better_auth_id="task_test_12345"
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    # Mock JWT token
    mock_jwt_token = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0YXNrX3Rlc3RfMTIzNDUiLCJlbWFpbCI6InRhc2tfdGVzdEBleGFtcGxlLmNvbSIsImV4cCI6OTk5OTk5OTk5OX0.test_signature"

    with patch('auth.jwt.verify_token') as mock_verify:
        mock_verify.return_value = {
            "sub": test_user.better_auth_id,
            "email": test_user.email,
            "exp": 9999999999
        }

        # Send POST request to /api/{user_id}/tasks with valid JWT and task payload
        task_payload = {
            "title": "Test Task",
            "description": "Test Description",
            "status": "incomplete"
        }
        response = client.post(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {mock_jwt_token}"},
            json=task_payload
        )

        # Verify response status code is 200
        assert response.status_code == 200

        # Verify response contains created task with correct user_id
        response_data = response.json()
        assert response_data["user_id"] == str(test_user.id)
        assert response_data["title"] == task_payload["title"]
        assert response_data["description"] == task_payload["description"]

        # Verify task is properly associated with authenticated user
        assert response_data["user_id"] == str(test_user.id)


def test_task_retrieval_for_specific_user(db_session, client):
    """Test Case 5: Task Retrieval for Specific User"""
    # Setup: Create authenticated user and multiple tasks
    test_user = User(
        email="retrieve_test@example.com",
        better_auth_id="retrieve_test_12345"
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    # Create multiple tasks for the user
    task1 = Task(
        user_id=test_user.id,
        title="Task 1",
        description="Description 1",
        status="incomplete"
    )
    task2 = Task(
        user_id=test_user.id,
        title="Task 2",
        description="Description 2",
        status="complete"
    )
    db_session.add(task1)
    db_session.add(task2)
    db_session.commit()

    # Mock JWT token
    mock_jwt_token = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyZXRyaWV2ZV90ZXN0XzEyMzQ1IiwiZW1haWwiOiJyZXRyaWV2ZV90ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjo5OTk5OTk5OTk5fQ.test_signature"

    with patch('auth.jwt.verify_token') as mock_verify:
        mock_verify.return_value = {
            "sub": test_user.better_auth_id,
            "email": test_user.email,
            "exp": 9999999999
        }

        # Send GET request to /api/{user_id}/tasks with valid JWT
        response = client.get(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )

        # Verify response status code is 200
        assert response.status_code == 200

        # Verify only tasks belonging to the specified user are returned
        response_data = response.json()
        assert len(response_data) == 2
        for task in response_data:
            assert task["user_id"] == str(test_user.id)


def test_individual_task_retrieval(db_session, client):
    """Test Case 6: Individual Task Retrieval"""
    # Setup: Create authenticated user and at least one task
    test_user = User(
        email="individual_test@example.com",
        better_auth_id="individual_test_12345"
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    task = Task(
        user_id=test_user.id,
        title="Individual Task",
        description="Individual Description",
        status="incomplete"
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    # Mock JWT token
    mock_jwt_token = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpbmRpdmlkdWFsX3Rlc3RfMTIzNDUiLCJlbWFpbCI6ImluZGl2aWR1YWxfdGVzdEBleGFtcGxlLmNvbSIsImV4cCI6OTk5OTk5OTk5OX0.test_signature"

    with patch('auth.jwt.verify_token') as mock_verify:
        mock_verify.return_value = {
            "sub": test_user.better_auth_id,
            "email": test_user.email,
            "exp": 9999999999
        }

        # Send GET request to /api/{user_id}/tasks/{task_id} with valid JWT
        response = client.get(
            f"/api/{test_user.id}/tasks/{task.id}",
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )

        # Verify response status code is 200
        assert response.status_code == 200

        # Verify returned task belongs to the specified user
        response_data = response.json()
        assert response_data["user_id"] == str(test_user.id)
        assert response_data["id"] == str(task.id)

        # Verify task data matches expected values
        assert response_data["title"] == task.title
        assert response_data["description"] == task.description
        assert response_data["status"] == task.status


def test_task_update_operations(db_session, client):
    """Test Case 7: Task Update Operations"""
    # Setup: Create authenticated user and a task to be updated
    test_user = User(
        email="update_test@example.com",
        better_auth_id="update_test_12345"
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    task = Task(
        user_id=test_user.id,
        title="Original Task",
        description="Original Description",
        status="incomplete"
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    # Mock JWT token
    mock_jwt_token = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1cGRhdGVfdGVzdF8xMjM0NSIsImVtYWlsIjoidXBkYXRlX3Rlc3RAZXhhbXBsZS5jb20iLCJleHAiOjk5OTk5OTk5OTl9.test_signature"

    with patch('auth.jwt.verify_token') as mock_verify:
        mock_verify.return_value = {
            "sub": test_user.better_auth_id,
            "email": test_user.email,
            "exp": 9999999999
        }

        # Send PUT request to /api/{user_id}/tasks/{task_id} with valid JWT and updated task data
        updated_data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "status": "complete"
        }
        response = client.put(
            f"/api/{test_user.id}/tasks/{task.id}",
            headers={"Authorization": f"Bearer {mock_jwt_token}"},
            json=updated_data
        )

        # Verify response status code is 200
        assert response.status_code == 200

        # Verify updated task data matches the request payload
        response_data = response.json()
        assert response_data["title"] == updated_data["title"]
        assert response_data["description"] == updated_data["description"]
        assert response_data["status"] == updated_data["status"]

        # Verify task remains associated with the correct user
        assert response_data["user_id"] == str(test_user.id)


def test_task_deletion_operations(db_session, client):
    """Test Case 8: Task Deletion Operations"""
    # Setup: Create authenticated user and a task to be deleted
    test_user = User(
        email="delete_test@example.com",
        better_auth_id="delete_test_12345"
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    task = Task(
        user_id=test_user.id,
        title="Task to Delete",
        description="Description to Delete",
        status="incomplete"
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    # Mock JWT token
    mock_jwt_token = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZWxldGVfdGVzdF8xMjM0NSIsImVtYWlsIjoiZGVsZXRlX3Rlc3RAZXhhbXBsZS5jb20iLCJleHAiOjk5OTk5OTk5OTl9.test_signature"

    with patch('auth.jwt.verify_token') as mock_verify:
        mock_verify.return_value = {
            "sub": test_user.better_auth_id,
            "email": test_user.email,
            "exp": 9999999999
        }

        # Send DELETE request to /api/{user_id}/tasks/{task_id} with valid JWT
        response = client.delete(
            f"/api/{test_user.id}/tasks/{task.id}",
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )

        # Verify response status code is 200
        assert response.status_code == 200

        # Verify task is successfully removed from database
        # Try to retrieve the deleted task
        deleted_task_response = client.get(
            f"/api/{test_user.id}/tasks/{task.id}",
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )
        assert deleted_task_response.status_code == 404


def test_task_completion_toggle(db_session, client):
    """Test Case 9: Task Completion Toggle"""
    # Setup: Create authenticated user and a task with initial status
    test_user = User(
        email="completion_test@example.com",
        better_auth_id="completion_test_12345"
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    task = Task(
        user_id=test_user.id,
        title="Completion Task",
        description="Description for completion",
        status="incomplete"
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    # Mock JWT token
    mock_jwt_token = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjb21wbGV0aW9uX3Rlc3RfMTIzNDUiLCJlbWFpbCI6ImNvbXBsZXRpb25fdGVzdEBleGFtcGxlLmNvbSIsImV4cCI6OTk5OTk5OTk5OX0.test_signature"

    with patch('auth.jwt.verify_token') as mock_verify:
        mock_verify.return_value = {
            "sub": test_user.better_auth_id,
            "email": test_user.email,
            "exp": 9999999999
        }

        # Send PATCH request to /api/{user_id}/tasks/{task_id}/complete with valid JWT and status payload
        status_payload = {"status": "complete"}
        response = client.patch(
            f"/api/{test_user.id}/tasks/{task.id}/complete",
            headers={"Authorization": f"Bearer {mock_jwt_token}"},
            json=status_payload
        )

        # Verify response status code is 200
        assert response.status_code == 200

        # Verify task status is updated to requested state
        response_data = response.json()
        assert response_data["task"]["status"] == status_payload["status"]

        # Verify response contains updated task with correct status
        assert response_data["task"]["id"] == str(task.id)
        assert response_data["task"]["status"] == "complete"


def test_cross_user_data_access_protection(db_session, client):
    """Test Case 10: Cross-User Data Access Protection"""
    # Setup: Create two different users with their respective tasks
    user1 = User(
        email="user1@example.com",
        better_auth_id="user1_12345"
    )
    user2 = User(
        email="user2@example.com",
        better_auth_id="user2_12345"
    )
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()
    db_session.refresh(user1)
    db_session.refresh(user2)

    task_for_user2 = Task(
        user_id=user2.id,
        title="User2's Task",
        description="Task belonging to user2",
        status="incomplete"
    )
    db_session.add(task_for_user2)
    db_session.commit()
    db_session.refresh(task_for_user2)

    # Mock JWT token for user1
    mock_jwt_token_user1 = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMV8xMjM0NSIsImVtYWlsIjoidXNlcjFAZXhhbXBsZS5jb20iLCJleHAiOjk5OTk5OTk5OTl9.test_signature"

    with patch('auth.jwt.verify_token') as mock_verify:
        mock_verify.return_value = {
            "sub": user1.better_auth_id,
            "email": user1.email,
            "exp": 9999999999
        }

        # Send GET request to /api/{user1_id}/tasks/{user2_task_id} with user1's JWT
        response = client.get(
            f"/api/{user1.id}/tasks/{task_for_user2.id}",
            headers={"Authorization": f"Bearer {mock_jwt_token_user1}"}
        )

        # Verify response status code is 403 Forbidden for cross-user access
        assert response.status_code == 403


def test_malformed_request_handling(db_session, client):
    """Test Case 11: Malformed Request Handling"""
    # Setup: Create authenticated user with valid JWT token
    test_user = User(
        email="malformed_test@example.com",
        better_auth_id="malformed_test_12345"
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    # Mock JWT token
    mock_jwt_token = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYWxmb3JtZWRfdGVzdF8xMjM0NSIsImVtYWlsIjoibWFsZm9ybWVkX3Rlc3RAZXhhbXBsZS5jb20iLCJleHAiOjk5OTk5OTk5OTl9.test_signature"

    with patch('auth.jwt.verify_token') as mock_verify:
        mock_verify.return_value = {
            "sub": test_user.better_auth_id,
            "email": test_user.email,
            "exp": 9999999999
        }

        # Send POST request to /api/{user_id}/tasks with invalid task payload
        invalid_payload = {
            "title": "",  # Invalid - empty title
            "description": "Valid description",
            "status": "invalid_status"  # Invalid status
        }
        response = client.post(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {mock_jwt_token}"},
            json=invalid_payload
        )

        # Verify response status code is 422 Unprocessable Entity
        assert response.status_code in [422, 400]  # Could be either depending on validation


def test_empty_state_handling(db_session, client):
    """Test Case 12: Empty State Handling"""
    # Setup: Create authenticated user with no existing tasks
    test_user = User(
        email="empty_test@example.com",
        better_auth_id="empty_test_12345"
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    # Mock JWT token
    mock_jwt_token = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlbXB0eV90ZXN0XzEyMzQ1IiwiZW1haWwiOiJlbXB0eV90ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjo5OTk5OTk5OTk5fQ.test_signature"

    with patch('auth.jwt.verify_token') as mock_verify:
        mock_verify.return_value = {
            "sub": test_user.better_auth_id,
            "email": test_user.email,
            "exp": 9999999999
        }

        # Send GET request to /api/{user_id}/tasks with valid JWT
        response = client.get(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )

        # Verify response status code is 200
        assert response.status_code == 200

        # Verify response is an empty array or appropriate empty state
        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) == 0


def test_jwt_token_expiration_and_validation(db_session, client):
    """Test Case 13: JWT Token Expiration and Validation"""
    # Setup: Obtain valid JWT token with short expiration time
    test_user = User(
        email="expired_test@example.com",
        better_auth_id="expired_test_12345"
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    # Mock expired JWT token
    expired_jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJleHBpcmVkX3Rlc3RfMTIzNDUiLCJlbWFpbCI6ImV4cGlyZWRfdGVzdEBleGFtcGxlLmNvbSIsImV4cCI6MTAwMH0.test_signature"  # Expired

    with patch('auth.jwt.verify_token') as mock_verify:
        # Simulate expired token by raising an exception
        mock_verify.side_effect = HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )

        # Send GET request to /api/auth/me with expired JWT
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {expired_jwt_token}"}
        )

        # Verify response status code is 401 Unauthorized
        assert response.status_code == 401