"""
Import Integrity Tests
Tests that all modules under src/app can be imported without errors
"""
import pytest
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def test_app_init_can_be_imported():
    """Test that the app package can be imported"""
    import app
    assert app is not None


def test_app_database_can_be_imported():
    """Test that the database module can be imported"""
    from app import database
    assert database is not None


def test_app_database_database_can_be_imported():
    """Test that the database.database module can be imported"""
    from app.database.database import engine, get_session
    assert engine is not None
    assert get_session is not None


def test_app_models_can_be_imported():
    """Test that all model modules can be imported"""
    from app.models.user import User
    from app.models.task import Task
    from app.models.conversation import Conversation
    from app.models.message import Message
    from app.models.ai_config import AIConfiguration
    from app.models.mcp_invocation import MCPToolInvocation

    assert User is not None
    assert Task is not None
    assert Conversation is not None
    assert Message is not None
    assert AIConfiguration is not None
    assert MCPToolInvocation is not None


def test_app_models_init_models_can_be_imported():
    """Test that the models init module can be imported"""
    from app.models.init_models import initialize_models
    assert initialize_models is not None


def test_app_auth_can_be_imported():
    """Test that auth modules can be imported"""
    from app.auth.jwt import get_current_user
    from app.auth.backend_jwt import get_current_user_from_backend_jwt, create_backend_jwt
    
    assert get_current_user is not None
    assert get_current_user_from_backend_jwt is not None
    assert create_backend_jwt is not None


def test_app_routes_can_be_imported():
    """Test that route modules can be imported"""
    from app.routes.auth import router as auth_router
    from app.routes.tasks import router as tasks_router
    
    assert auth_router is not None
    assert tasks_router is not None


def test_app_api_can_be_imported():
    """Test that API modules can be imported"""
    from app.api.chat_router import router as chat_router
    
    assert chat_router is not None


def test_app_services_can_be_imported():
    """Test that service modules can be imported"""
    from app.services.ai_agent_service import AIAgentService
    from app.services.conversation_service import ConversationService
    from app.services.validation import ValidationService
    from app.services.mcp_server import MCPServer
    from app.services.ai_provider_factory import AIProviderFactory
    from app.services.tool_registry import ToolRegistry
    
    assert AIAgentService is not None
    assert ConversationService is not None
    assert ValidationService is not None
    assert MCPServer is not None
    assert AIProviderFactory is not None
    assert ToolRegistry is not None


def test_app_config_can_be_imported():
    """Test that config modules can be imported"""
    from app.config.ai_settings import AISettings
    
    assert AISettings is not None


def test_app_utils_can_be_imported():
    """Test that util modules can be imported"""
    from app.utils.validation import validate_uuid, validate_user_id_match
    from app.utils.logging import app_logger, log_ai_provider_config
    
    assert validate_uuid is not None
    assert validate_user_id_match is not None
    assert app_logger is not None
    assert log_ai_provider_config is not None


def test_app_core_can_be_imported():
    """Test that core modules can be imported"""
    from app.core.config import get_ai_config, AIConfig

    assert get_ai_config is not None
    assert AIConfig is not None


def test_app_schemas_can_be_imported():
    """Test that schema modules can be imported"""
    from app.schemas.user import UserCreate, UserRead
    from app.schemas.task import TaskCreate, TaskRead, TaskUpdate, TaskComplete
    
    assert UserCreate is not None
    assert UserRead is not None
    assert TaskCreate is not None
    assert TaskRead is not None
    assert TaskUpdate is not None
    assert TaskComplete is not None


def test_app_database_add_better_auth_id_column_can_be_imported():
    """Test that database migration modules can be imported"""
    from app.database.add_better_auth_id_column import add_better_auth_id_column

    assert add_better_auth_id_column is not None


def test_app_database_migrations_can_be_imported():
    """Test that database migration modules can be imported"""
    from app.database.migrations import run_migrations
    
    assert run_migrations is not None


def test_app_services_ai_validation_can_be_imported():
    """Test that AI validation modules can be imported"""
    from app.services.ai_validation import AIValidationService

    assert AIValidationService is not None


def test_app_services_error_handler_can_be_imported():
    """Test that error handler modules can be imported"""
    from app.services.error_handler import ErrorHandler
    
    assert ErrorHandler is not None


def test_app_services_fallback_handler_can_be_imported():
    """Test that fallback handler modules can be imported"""
    from app.services.fallback_handler import FallbackHandler, CircuitBreaker
    
    assert FallbackHandler is not None
    assert CircuitBreaker is not None