"""
FastAPI Boot Tests
Tests that the FastAPI application can boot successfully with all components
"""
import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def test_main_app_can_be_imported():
    """Test that the main app module can be imported"""
    from backend import main
    assert main is not None


def test_fastapi_app_instance_creation():
    """Test that the FastAPI app can be instantiated"""
    from backend.main import app
    assert app is not None
    assert hasattr(app, 'routes')
    assert hasattr(app, 'middleware')


def test_app_has_correct_title():
    """Test that the app has the correct title"""
    from backend.main import app
    assert app.title == "Todo API"


def test_app_has_correct_description():
    """Test that the app has the correct description"""
    from backend.main import app
    assert "multi-user todo application with AI chatbot" in app.description


def test_app_has_health_route():
    """Test that the app has the health check route"""
    from backend.main import app
    health_route_found = False
    for route in app.routes:
        if hasattr(route, 'path') and route.path == "/health":
            health_route_found = True
            break
    assert health_route_found


def test_app_has_root_route():
    """Test that the app has the root route"""
    from backend.main import app
    root_route_found = False
    for route in app.routes:
        if hasattr(route, 'path') and route.path == "/":
            root_route_found = True
            break
    assert root_route_found


def test_app_has_cors_middleware():
    """Test that the app has CORS middleware"""
    from backend.main import app
    cors_middleware_found = False
    for middleware in app.user_middleware:
        if hasattr(middleware, 'cls'):
            # Check if it's the CORSMiddleware
            if 'CORSMiddleware' in str(middleware.cls):
                cors_middleware_found = True
                break
    assert cors_middleware_found


def test_auth_routes_loaded():
    """Test that auth routes are loaded"""
    from backend.main import app
    auth_routes_found = False
    for route in app.routes:
        if hasattr(route, 'path') and '/api/auth' in route.path:
            auth_routes_found = True
            break
    assert auth_routes_found


def test_task_routes_loaded():
    """Test that task routes are loaded"""
    from backend.main import app
    task_routes_found = False
    for route in app.routes:
        if hasattr(route, 'path') and '/api/' in route.path and route.path != '/api/auth':
            task_routes_found = True
            break
    assert task_routes_found


def test_chat_routes_loaded():
    """Test that chat routes are loaded"""
    from backend.main import app
    chat_routes_found = False
    for route in app.routes:
        if hasattr(route, 'path') and '/api/v1/chat' in route.path:
            chat_routes_found = True
            break
    assert chat_routes_found