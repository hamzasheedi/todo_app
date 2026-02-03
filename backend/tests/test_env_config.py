"""
Environment Configuration Tests
Tests that environment variables are properly loaded and validated
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


def test_ai_provider_env_var_exists():
    """Test that AI_PROVIDER environment variable exists"""
    assert os.getenv('AI_PROVIDER') is not None


def test_ai_base_url_env_var_exists():
    """Test that AI_BASE_URL environment variable exists"""
    assert os.getenv('AI_BASE_URL') is not None


def test_ai_api_key_env_var_exists():
    """Test that AI_API_KEY environment variable exists"""
    assert os.getenv('AI_API_KEY') is not None


def test_ai_model_env_var_exists():
    """Test that AI_MODEL environment variable exists"""
    assert os.getenv('AI_MODEL') is not None


def test_database_url_env_var_exists():
    """Test that DATABASE_URL environment variable exists"""
    assert os.getenv('DATABASE_URL') is not None


def test_ai_settings_loads_from_env():
    """Test that AI settings loads from environment variables"""
    from app.config.ai_settings import AISettings
    assert AISettings.AI_PROVIDER is not None
    assert AISettings.AI_BASE_URL is not None
    assert AISettings.AI_API_KEY is not None
    assert AISettings.AI_MODEL is not None


def test_ai_settings_default_values():
    """Test that AI settings has proper default values"""
    from app.config.ai_settings import AISettings
    assert hasattr(AISettings, 'AI_TIMEOUT')
    assert isinstance(AISettings.AI_TIMEOUT, int)


def test_ai_settings_fallback_values():
    """Test that AI settings has fallback values"""
    from app.config.ai_settings import AISettings
    assert hasattr(AISettings, 'FALLBACK_AI_BASE_URL')
    assert hasattr(AISettings, 'FALLBACK_AI_API_KEY')


def test_groq_provider_configured():
    """Test that groq provider is properly configured if selected"""
    from app.config.ai_settings import AISettings
    if AISettings.AI_PROVIDER == 'groq':
        assert 'groq' in AISettings.AI_BASE_URL.lower()


def test_env_variables_properly_set():
    """Test that all required environment variables are properly set"""
    required_vars = [
        'AI_PROVIDER',
        'AI_BASE_URL', 
        'AI_API_KEY',
        'AI_MODEL',
        'DATABASE_URL'
    ]
    
    for var in required_vars:
        assert os.getenv(var) is not None, f"Environment variable {var} is not set"