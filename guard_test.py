#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Guard test to verify that the application is properly configured for the backend/src/app layout.
"""

import sys
from pathlib import Path

def test_app_importable():
    """Test that the app can be imported with correct path configuration"""
    
    # Add the backend/src/app directory to the Python path
    current_dir = Path(__file__).parent
    backend_path = current_dir / "backend"
    src_path = backend_path / "src"
    app_path = src_path / "app"

    # Add paths to Python path in the correct order
    for path in [str(app_path), str(src_path), str(backend_path)]:
        if path not in sys.path:
            sys.path.insert(0, path)

    # Test importing the main backend module
    try:
        import backend.main
        print("OK: backend.main imported successfully")
    except ImportError as e:
        print(f"ERROR: Failed to import backend.main: {e}")
        return False

    # Test importing app modules
    try:
        from app.auth import get_current_user
        from app.models.user import User
        from app.services.ai_agent_service import AIAgentService
        from app.routes.auth import router as auth_router
        from app.routes.tasks import router as tasks_router
        from app.api.chat_router import router as chat_router
        print("OK: All app modules imported successfully")
    except ImportError as e:
        print(f"ERROR: Failed to import app modules: {e}")
        return False

    # Test that the main app instance exists
    try:
        app = backend.main.app
        assert app is not None
        print("OK: FastAPI app instance exists")
    except AttributeError:
        print("ERROR: FastAPI app instance does not exist")
        return False

    return True

if __name__ == "__main__":
    success = test_app_importable()
    if success:
        print("\nAll tests passed!")
        print("FastAPI startup is correctly configured for the backend/src/app layout. All imports resolve successfully.")
    else:
        print("\nSome tests failed!")
        sys.exit(1)