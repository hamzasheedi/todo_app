#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import validation tests for the Todo API application.

This script validates that all required imports work correctly with the src/app layout.
"""

import sys
from pathlib import Path

def test_imports():
    """Test that all required imports work correctly"""

    # Add the project paths to sys.path
    project_root = Path(__file__).parent
    backend_path = project_root / "backend"
    src_path = backend_path / "src"
    app_path = src_path / "app"

    # Add paths to Python path in the correct order
    for path in [str(app_path), str(src_path), str(backend_path), str(project_root)]:
        if path not in sys.path:
            sys.path.insert(0, path)

    print("Testing import resolution for src/app layout...")

    # Test main app import
    try:
        from app.main import app
        print("OK app.main imported successfully")
    except ImportError as e:
        print(f"ERROR Failed to import app.main: {e}")
        return False
    
    # Test auth imports
    try:
        from app.auth import get_current_user
        from app.auth.jwt import get_current_user as jwt_get_current_user
        from app.auth.backend_jwt import get_current_user_from_backend_jwt
        print("OK app.auth imports successful")
    except ImportError as e:
        print(f"ERROR Failed to import app.auth: {e}")
        return False

    # Test routes imports
    try:
        from app.routes.auth import router as auth_router
        from app.routes.tasks import router as tasks_router
        from app.api.chat_router import router as chat_router
        print("OK app.routes imports successful")
    except ImportError as e:
        print(f"ERROR Failed to import app.routes: {e}")
        return False

    # Test services imports
    try:
        from app.services.ai_agent_service import AIAgentService
        from app.services.conversation_service import ConversationService
        from app.services.validation import ValidationService
        from app.services.mcp_server import MCPServer
        print("OK app.services imports successful")
    except ImportError as e:
        print(f"ERROR Failed to import app.services: {e}")
        return False

    # Test models imports
    try:
        from app.models.user import User
        from app.models.task import Task
        from app.models.conversation import Conversation
        from app.models.message import Message
        print("OK app.models imports successful")
    except ImportError as e:
        print(f"ERROR Failed to import app.models: {e}")
        return False

    # Test config imports
    try:
        from app.config.ai_settings import AISettings
        print("OK app.config imports successful")
    except ImportError as e:
        print(f"ERROR Failed to import app.config: {e}")
        return False

    # Test database imports
    try:
        from app.database.database import create_db_and_tables, get_session
        print("OK app.database imports successful")
    except ImportError as e:
        print(f"ERROR Failed to import app.database: {e}")
        return False

    print("\nOK All imports resolved successfully!")
    print("FastAPI startup is correctly configured for src/app layout.")
    return True

if __name__ == "__main__":
    success = test_imports()
    if not success:
        sys.exit(1)