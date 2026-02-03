"""
Configuration for pytest
"""
import os
import sys
from pathlib import Path

# Add the project root directory to the path so tests can import modules
project_root = Path(__file__).parent.parent  # Go up twice to reach project root
src_path = project_root / "src"
app_path = src_path / "app"

# Add paths to Python path in the correct order
if str(app_path) not in sys.path:
    sys.path.insert(0, str(app_path))
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Set environment variables for testing
os.environ.setdefault('AI_PROVIDER', 'groq')
os.environ.setdefault('AI_BASE_URL', 'https://api.groq.com/openai/v1')
os.environ.setdefault('AI_API_KEY', 'test-key')
os.environ.setdefault('AI_MODEL', 'llama3-70b-8192')
os.environ.setdefault('AI_TIMEOUT', '30')
os.environ.setdefault('FALLBACK_AI_BASE_URL', 'https://api.openai.com/v1')
os.environ.setdefault('FALLBACK_AI_API_KEY', 'test-fallback-key')
os.environ.setdefault('DATABASE_URL', 'sqlite:///./test_todo_app.db')
os.environ.setdefault('AUTH_SECRET', 'test-secret')
os.environ.setdefault('JWT_SECRET', 'test-jwt-secret')
os.environ.setdefault('ENVIRONMENT', 'testing')