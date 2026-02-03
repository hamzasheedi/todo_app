#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Canonical startup script for the Todo API application with AI Chatbot.

This script ensures the correct Python path for the src/app layout.
"""

import os
import sys
from pathlib import Path

def main():
    # Add the project root to Python path
    project_root = Path(__file__).parent.resolve()
    backend_path = project_root / "backend"
    src_path = backend_path / "src"
    app_path = src_path / "app"

    # Add paths to Python path in the correct order
    if str(app_path) not in sys.path:
        sys.path.insert(0, str(app_path))
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    # Verify that app modules can be imported
    try:
        from app.main import app
        print("✓ App modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import app modules: {e}")
        print("Ensure the backend/src/app directory contains all application modules.")
        sys.exit(1)

    print("Starting Todo API with AI Chatbot...")
    print("Available endpoints:")
    print("  - GET / (health check)")
    print("  - GET /health (health check)")
    print("  - POST /api/v1/chat (AI chat functionality)")
    print("  - Auth and task endpoints (with JWT protection)")
    print("\nChat endpoint configured with OpenAI Agents SDK and MCP tools")
    print("All task mutations routed through MCP server for security")

    # Start the application
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        app_dir=str(src_path)
    )

if __name__ == "__main__":
    main()