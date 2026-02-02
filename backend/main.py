#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main entry point for the Todo API application.

This file can be run directly or as a module.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path to resolve imports properly
# Since we're running from the backend directory, the src directory is a subdirectory
current_dir = Path(__file__).parent
src_path = current_dir / "src"
app_path = src_path / "app"

# Add paths to Python path in the correct order
# Insert in reverse order to ensure correct precedence
if str(app_path) not in sys.path:
    sys.path.insert(0, str(app_path))
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Force reload of sys.modules to clear any cached incorrect imports
for module_name in list(sys.modules.keys()):
    if module_name.startswith('app.'):
        del sys.modules[module_name]

# Verify that app modules can be imported
try:
    # Test importing some core app modules to verify path is set correctly
    from app.auth import get_current_user
    from app.models.user import User
    from app.services.ai_agent_service import AIAgentService
    print("OK App modules can be imported successfully")
except ImportError as e:
    print(f"ERROR Failed to import app modules: {e}")
    print("Make sure the backend/src/app directory contains all application modules.")
    sys.exit(1)

# Now we can import using absolute imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Todo API",
    description="API for the multi-user todo application with AI chatbot",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],  # Allow frontend and backend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose headers that browsers are allowed to access
    expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials"]
)

@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    try:
        from app.database.database import create_db_and_tables
        create_db_and_tables()
    except ImportError:
        print("Warning: Could not create database tables")

@app.get("/")
def read_root():
    return {"message": "Todo API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Include the auth and task routes from the app structure
try:
    from app.routes.auth import router as auth_router
    from app.routes.tasks import router as tasks_router
    app.include_router(auth_router)
    app.include_router(tasks_router, prefix="/api")
    print("Auth and task routes loaded successfully")
except ImportError as e:
    print(f"Warning: Could not import auth and tasks routes: {e}")

# Include Chat functionality from the new app structure
try:
    from app.api.chat_router import router as chat_router
    # Use /api/v1/chat prefix as required by the specification
    app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])
    print("Chat endpoints loaded successfully with AI integration")
except ImportError as e:
    print(f"Warning: Chat endpoints not available: {e}")
except Exception as e:
    print(f"Warning: Could not load chat endpoints: {e}")
    print("Continuing with core functionality only")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)