"""
Module to initialize models and avoid duplicate SQLAlchemy table definitions.
"""

from sqlmodel import SQLModel

# Import all models to register them with SQLModel
from .ai_config import AIConfiguration
from .conversation import Conversation
from .mcp_invocation import MCPToolInvocation
from .user import User
from .task import Task
from .message import Message

# Export all models
__all__ = ["AIConfig", "Conversation", "MCPToolInvocation", "User", "Task", "Message"]

# Flag to track if models have been initialized
_models_initialized = False

def initialize_models():
    """Initialize models to register them with SQLModel metadata."""
    global _models_initialized
    if not _models_initialized:
        # Trigger registration of all models with SQLModel
        _models_initialized = True