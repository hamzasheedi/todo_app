import pytest
from httpx import AsyncClient
from main import app  # FastAPI app
import jwt
import os

# Use environment variables for JWT secret
JWT_SECRET = os.getenv("BETTER_AUTH_SECRET", "secret_key_for_testing")

@pytest.mark.asyncio
async def test_signup_login_and_task_flow():
    """
    Full backend test: signup, login, JWT verification, task CRUD
    """

    async with AsyncClient(app=app, base_url="http://testserver") as client:

        # Action: Send signup request
        signup_data = {"email": "testuser@example.com", "password": "password123"}
        response = await client.post("/api/auth/sign-up/email", json=signup_data)
        assert response.status_code == 201, "Signup should succeed"

        # Action: Send login request
        login_data = {"email": "testuser@example.com", "password": "password123"}
        response = await client.post("/api/auth/sign-in/email", json=login_data)
        assert response.status_code == 200, "Login should succeed"
        token = response.json().get("access_token")
        assert token is not None, "JWT token should be returned"

        # Action: Decode JWT token
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        assert user_id is not None, "JWT token should contain user ID"

        headers = {"Authorization": f"Bearer {token}"}

        # Action: Create a new task
        task_data = {"title": "Test Task", "description": "Task description"}
        response = await client.post(f"/api/{user_id}/tasks", json=task_data, headers=headers)
        assert response.status_code == 201, "Task creation should succeed"
        task_id = response.json().get("id")

        # Action: Get all tasks for the user
        response = await client.get(f"/api/{user_id}/tasks", headers=headers)
        assert response.status_code == 200, "Fetching tasks should succeed"
        tasks = response.json()
        assert any(t["id"] == task_id for t in tasks), "Created task should be in the list"

        # Action: Update task
        update_data = {"title": "Updated Task Title"}
        response = await client.put(f"/api/{user_id}/tasks/{task_id}", json=update_data, headers=headers)
        assert response.status_code == 200, "Task update should succeed"
        assert response.json()["title"] == "Updated Task Title"

        # Action: Toggle task completion
        response = await client.patch(f"/api/{user_id}/tasks/{task_id}/complete", headers=headers)
        assert response.status_code == 200, "Toggle completion should succeed"
        assert response.json()["completed"] is True

        # Action: Delete task
        response = await client.delete(f"/api/{user_id}/tasks/{task_id}", headers=headers)
        assert response.status_code == 200, "Task deletion should succeed"

        # Action: Verify task is deleted
        response = await client.get(f"/api/{user_id}/tasks/{task_id}", headers=headers)
        assert response.status_code == 404, "Deleted task should not exist"

        # Action: Verify access without token fails
        response = await client.get(f"/api/{user_id}/tasks")
        assert response.status_code == 401, "Requests without JWT should be unauthorized"