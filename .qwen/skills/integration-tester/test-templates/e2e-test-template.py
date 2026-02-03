import pytest
import asyncio
from playwright.async_api import async_playwright
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app
from backend.database import get_session
from backend.models import User, Task
from backend.config import settings
import jwt
import os
from datetime import datetime, timedelta

# For integration testing with real database
SQLALCHEMY_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class IntegrationTestTemplate:
    """
    Comprehensive integration test template for end-to-end testing
    """

    def __init__(self):
        self.client = TestClient(app)
        self.db = TestingSessionLocal()

    def setup_method(self):
        """
        Setup method for integration tests
        """
        # Create a test user
        self.test_user = User(
            email="integration-test@example.com",
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )
        self.db.add(self.test_user)
        self.db.commit()
        self.db.refresh(self.test_user)

        # Generate a test JWT token
        self.test_token = self.generate_test_token(self.test_user.id)

    def teardown_method(self):
        """
        Teardown method to clean up test data
        """
        # Clean up tasks first (due to foreign key constraint)
        self.db.query(Task).filter(Task.user_id == self.test_user.id).delete()
        # Then clean up user
        self.db.query(User).filter(User.id == self.test_user.id).delete()
        self.db.commit()
        self.db.close()

    def generate_test_token(self, user_id: str) -> str:
        """
        Generate a test JWT token
        """
        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow()
        }
        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return token

    def test_full_user_flow(self):
        """
        Test complete user flow: authentication -> task creation -> task management -> cleanup
        """
        # Step 1: Test authentication (if applicable)
        auth_headers = {"Authorization": f"Bearer {self.test_token}"}

        # Step 2: Create a task
        task_data = {
            "title": "Integration Test Task",
            "description": "This is a test task for integration testing",
            "status": "incomplete"
        }
        response = self.client.post(
            f"/api/{self.test_user.id}/tasks",
            json=task_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        created_task = response.json()
        task_id = created_task["id"]
        assert created_task["title"] == task_data["title"]

        # Step 3: Retrieve the task
        response = self.client.get(
            f"/api/{self.test_user.id}/tasks/{task_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        retrieved_task = response.json()
        assert retrieved_task["id"] == task_id

        # Step 4: Update the task
        update_data = {
            "title": "Updated Integration Test Task",
            "description": "Updated description for integration test",
            "status": "complete"
        }
        response = self.client.put(
            f"/api/{self.test_user.id}/tasks/{task_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["title"] == update_data["title"]
        assert updated_task["status"] == update_data["status"]

        # Step 5: List all tasks
        response = self.client.get(
            f"/api/{self.test_user.id}/tasks",
            headers=auth_headers
        )
        assert response.status_code == 200
        tasks_list = response.json()
        assert len(tasks_list) >= 1
        assert any(task["id"] == task_id for task in tasks_list)

        # Step 6: Delete the task
        response = self.client.delete(
            f"/api/{self.test_user.id}/tasks/{task_id}",
            headers=auth_headers
        )
        assert response.status_code == 200

    def test_user_isolation(self):
        """
        Test that users cannot access other users' tasks
        """
        # Create another test user
        other_user = User(
            email="other-test@example.com",
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )
        self.db.add(other_user)
        self.db.commit()
        self.db.refresh(other_user)

        # Create a task for the main user
        task_data = {
            "title": "Main User Task",
            "description": "Task for main user",
            "status": "incomplete"
        }
        response = self.client.post(
            f"/api/{self.test_user.id}/tasks",
            json=task_data,
            headers={"Authorization": f"Bearer {self.test_token}"}
        )
        assert response.status_code == 200
        task = response.json()
        task_id = task["id"]

        # Generate token for other user
        other_token = self.generate_test_token(other_user.id)

        # Try to access main user's task with other user's token
        response = self.client.get(
            f"/api/{self.test_user.id}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {other_token}"}
        )
        # Should fail due to user isolation
        assert response.status_code in [403, 404]  # Forbidden or Not Found

        # Cleanup
        self.db.delete(other_user)
        self.db.commit()

    def test_error_handling(self):
        """
        Test error handling across different scenarios
        """
        auth_headers = {"Authorization": f"Bearer {self.test_token}"}

        # Test invalid task data
        invalid_task_data = {
            "title": "",  # Invalid: empty title
            "description": "Valid description"
        }
        response = self.client.post(
            f"/api/{self.test_user.id}/tasks",
            json=invalid_task_data,
            headers=auth_headers
        )
        assert response.status_code == 422

        # Test non-existent task access
        response = self.client.get(
            f"/api/{self.test_user.id}/tasks/non-existent-id",
            headers=auth_headers
        )
        assert response.status_code == 404

        # Test unauthorized access
        response = self.client.get(f"/api/{self.test_user.id}/tasks")
        assert response.status_code == 401


class E2ETestTemplate:
    """
    End-to-end browser testing template using Playwright
    """

    async def test_frontend_authentication_flow(self):
        """
        Test the complete authentication flow in the frontend
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                # Navigate to login page
                await page.goto("http://localhost:3000/login")

                # Fill in login form
                await page.fill('input[name="email"]', 'test@example.com')
                await page.fill('input[name="password"]', 'password123')
                await page.click('button[type="submit"]')

                # Wait for navigation to dashboard
                await page.wait_for_url("**/tasks")

                # Verify user is logged in by checking for user-specific elements
                await page.wait_for_selector("text=My Tasks")

                # Test task creation
                await page.click("text=Add New Task")
                await page.fill('input[placeholder="Task Title"]', 'E2E Test Task')
                await page.fill('textarea[placeholder="Task Description"]', 'Created via E2E test')
                await page.click("text=Create Task")

                # Verify task appears in list
                await page.wait_for_selector("text=E2E Test Task")

                # Test task completion
                complete_button = page.locator("button:has-text('Complete')")
                await complete_button.click()

                # Verify task status changed
                await page.wait_for_selector("text=Status: Complete")

                # Test task deletion
                delete_button = page.locator("button:has-text('Delete')")
                await delete_button.click()

                # Verify task is removed
                await page.wait_for_timeout(1000)  # Wait for deletion to complete
                assert not await page.is_visible("text=E2E Test Task")

            finally:
                await browser.close()

    async def test_responsive_design(self):
        """
        Test responsive design across different screen sizes
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            # Test mobile view
            mobile_context = await browser.new_context(
                viewport={"width": 375, "height": 667}  # iPhone SE
            )
            mobile_page = await mobile_context.new_page()

            await mobile_page.goto("http://localhost:3000/tasks")

            # Verify mobile-specific elements are visible
            await mobile_page.wait_for_selector("text=Menu")  # Hamburger menu should be visible
            assert await mobile_page.is_visible("button:text('Add')")  # Should be abbreviated on mobile

            # Test tablet view
            tablet_context = await browser.new_context(
                viewport={"width": 768, "height": 1024}  # iPad
            )
            tablet_page = await tablet_context.new_page()

            await tablet_page.goto("http://localhost:3000/tasks")

            # Verify tablet-specific layout
            # Add tablet-specific assertions here

            await mobile_context.close()
            await tablet_context.close()
            await browser.close()

    async def test_accessibility(self):
        """
        Test accessibility features
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            await page.goto("http://localhost:3000/tasks")

            # Test keyboard navigation
            await page.keyboard.press("Tab")  # Focus should move to first interactive element
            focused_element = await page.evaluate("document.activeElement.tagName")
            assert focused_element in ["A", "BUTTON", "INPUT"]  # Should be an interactive element

            # Test ARIA attributes
            # Check for proper ARIA labels and roles
            has_proper_labels = await page.evaluate("""
                () => {
                    const inputs = document.querySelectorAll('input[aria-label]');
                    return inputs.length > 0;
                }
            """)
            assert has_proper_labels

            await browser.close()


# Pytest configuration for integration tests
@pytest.mark.integration
class TestIntegrationScenarios(IntegrationTestTemplate):
    pass


@pytest.mark.e2e
class TestE2EScenarios(E2ETestTemplate):
    pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])