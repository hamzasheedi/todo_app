"""
Runtime Smoke Tests
Tests that simulate the core application functionality
"""
import pytest
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def test_ai_agent_service_initialization():
    """Test that AI agent service can be initialized"""
    from app.services.ai_agent_service import AIAgentService
    ai_agent = AIAgentService()
    assert ai_agent is not None


def test_conversation_service_initialization():
    """Test that conversation service can be initialized"""
    from app.services.conversation_service import ConversationService
    conversation_service = ConversationService()
    assert conversation_service is not None


def test_validation_service_initialization():
    """Test that validation service can be initialized"""
    from app.services.validation import ValidationService
    validation_service = ValidationService()
    assert validation_service is not None


def test_ai_provider_factory_initialization():
    """Test that AI provider factory can be initialized"""
    from app.services.ai_provider_factory import AIProviderFactory
    factory = AIProviderFactory()
    assert factory is not None


def test_database_session_creation():
    """Test that database session can be created"""
    from app.database.database import get_session
    session_gen = get_session()
    session = next(session_gen)
    assert session is not None
    # Close the session
    session.close()


def test_user_model_creation():
    """Test that user model can be instantiated"""
    from app.models.init_models import initialize_models
    initialize_models()  # Initialize models to resolve relationships
    from app.models.user import User
    import uuid
    user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        better_auth_id="test_auth_id",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    assert user.email == "test@example.com"


def test_task_model_creation():
    """Test that task model can be instantiated"""
    from app.models.init_models import initialize_models
    initialize_models()  # Initialize models to resolve relationships
    from app.models.task import Task
    import uuid
    task = Task(
        id=uuid.uuid4(),
        title="Test Task",
        description="Test Description",
        status="incomplete",
        user_id=uuid.uuid4(),
        created_date=datetime.now(),
        updated_date=datetime.now()
    )
    assert task.title == "Test Task"


def test_conversation_model_creation():
    """Test that conversation model can be instantiated"""
    from app.models.init_models import initialize_models
    initialize_models()  # Initialize models to resolve relationships
    from app.models.conversation import Conversation
    import uuid
    conversation = Conversation(
        id=uuid.uuid4(),
        title="Test Conversation",
        user_id=uuid.uuid4(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    assert conversation.title == "Test Conversation"


def test_message_model_creation():
    """Test that message model can be instantiated"""
    from app.models.init_models import initialize_models
    initialize_models()  # Initialize models to resolve relationships
    from app.models.message import Message
    import uuid
    message = Message(
        id=uuid.uuid4(),
        content="Test message content",
        role="user",
        conversation_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        timestamp=datetime.now()
    )
    assert message.content == "Test message content"


def test_ai_agent_processes_message():
    """Test that AI agent can be initialized and has required methods"""
    from app.services.ai_agent_service import AIAgentService

    ai_agent = AIAgentService()
    assert ai_agent is not None
    assert hasattr(ai_agent, 'process_user_message')
    assert hasattr(ai_agent, 'primary_client')


def test_conversation_service_creates_conversation():
    """Test that conversation service can create a conversation"""
    from app.services.conversation_service import ConversationService
    from app.database.database import SessionLocal
    import uuid
    
    # Create a mock session
    session = Mock()
    session.add = Mock()
    session.commit = Mock()
    session.refresh = Mock()
    
    user_id = uuid.uuid4()
    conversation = ConversationService.create_conversation(session, user_id, "Test Title")
    
    # Verify that session.add was called
    session.add.assert_called_once()
    assert conversation.title == "Test Title"


def test_validation_service_validates_message():
    """Test that validation service can validate a message"""
    from app.services.validation import ValidationService
    
    # This should not raise an exception
    ValidationService.validate_ai_request("This is a valid message")
    
    # Test with an empty message (should raise an exception)
    with pytest.raises(ValueError):
        ValidationService.validate_ai_request("")
    
    # Test with a very long message (should raise an exception)
    with pytest.raises(ValueError):
        ValidationService.validate_ai_request("x" * 501)


def test_error_handler_initialization():
    """Test that error handler can be initialized"""
    from app.services.error_handler import ErrorHandler
    handler = ErrorHandler()
    assert handler is not None


def test_response_formatter_initialization():
    """Test that response formatter can be initialized"""
    from app.services.response_formatter import ResponseFormatter
    formatter = ResponseFormatter()
    assert formatter is not None


def test_timeout_handler_initialization():
    """Test that timeout handler can be initialized"""
    from app.services.timeout_handler import TimeoutManager
    manager = TimeoutManager()
    assert manager is not None