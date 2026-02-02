#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main FastAPI application instance for the Todo API with AI Chatbot.

This module defines the FastAPI app instance and includes all routes.
Other modules can import this as 'from app.main import app'.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create the FastAPI app instance
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
    """Create database tables and validate AI configuration on startup"""
    try:
        from app.database.database import create_db_and_tables
        create_db_and_tables()
    except ImportError:
        print("Warning: Could not create database tables")

    # Validate AI configuration
    try:
        from app.config.ai_settings import AISettings
        AISettings.validate_configuration()
        print(f"AI Configuration validated: {AISettings.AI_PROVIDER} provider selected")
        print(f"Model: {AISettings.AI_MODEL}")
    except ValueError as e:
        print(f"AI Configuration Error: {e}")
        print("Please set the required environment variables for your chosen AI provider.")

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

    # Also include user-specific chat route as per specification
    # This would be handled in the chat_router itself with a dynamic path
except ImportError as e:
    print(f"Warning: Could not import chat endpoints: {e}")
except Exception as e:
    print(f"Warning: Could not load chat endpoints: {e}")
    print("Continuing with core functionality only")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)