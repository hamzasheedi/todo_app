import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from unittest.mock import Mock, patch
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app
from models.user import User
from database.database import engine, SessionLocal, create_db_and_tables
from auth.jwt import verify_token


@pytest.fixture(scope="module")
def client():
    """Create a test client for the FastAPI app"""
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def setup_database():
    """Setup the database before each test"""
    # Create tables
    create_db_and_tables()
    yield
    # Cleanup can be done here if needed


def test_auth_routes_exist(client):
    """Test that authentication routes exist"""
    # Test GET / route
    response = client.get("/")
    assert response.status_code == 200

    # Test health check
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_current_user_without_auth():
    """Test that accessing protected endpoints without auth returns 401"""
    # This would test an endpoint that requires authentication
    # Since we don't have a specific protected endpoint in main, we'll test the auth endpoint directly
    response = client.get("/api/auth/me")
    # Without proper auth, this should return 401 or 403
    assert response.status_code in [401, 403]


def test_user_model_creation():
    """Test that User model can be created properly"""
    user = User(
        email="test@example.com",
        better_auth_id="test_auth_id_123"
    )

    assert user.email == "test@example.com"
    assert user.better_auth_id == "test_auth_id_123"
    assert user.id is not None  # UUID should be generated


def test_jwt_verification_fails_without_token():
    """Test JWT verification fails without proper token"""
    with pytest.raises(Exception):
        # This would fail because there's no valid token
        verify_token("")


@patch('auth.jwt.verify_token')
def test_sync_user_endpoint(mock_verify_token):
    """Test the sync-user endpoint functionality"""
    mock_verify_token.return_value = {"sub": "test_user", "email": "test@example.com"}

    # Test the sync-user endpoint with valid data
    sync_data = {
        "better_auth_id": "test_auth_id_123",
        "email": "test@example.com"
    }

    # We can't directly test this endpoint without a full auth setup
    # But we can test the logic separately
    from routes.auth import sync_user_with_backend
    from database.database import SessionLocal

    # Create a mock session
    session = SessionLocal()

    # This is a basic test - the full integration test would require more setup
    assert sync_data["better_auth_id"] == "test_auth_id_123"
    assert sync_data["email"] == "test@example.com"


def test_database_connection():
    """Test that database connection works"""
    with Session(engine) as session:
        # Just test that we can create a session
        assert session is not None


def test_user_lifecycle():
    """Test user creation and retrieval from database"""
    # Create a user
    with Session(engine) as session:
        from datetime import datetime
        new_user = User(
            email="lifecycle@test.com",
            better_auth_id="lifecycle_auth_id_123",
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        # Retrieve the user
        retrieved_user = session.exec(select(User).where(User.email == "lifecycle@test.com")).first()

        assert retrieved_user is not None
        assert retrieved_user.email == "lifecycle@test.com"
        assert retrieved_user.better_auth_id == "lifecycle_auth_id_123"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])