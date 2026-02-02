"""
AI Configuration Model
Represents the configuration for AI provider selection, including base_url, API key, and provider type
"""

from sqlmodel import SQLModel, Field
from typing import Optional
import uuid


class AIConfiguration(SQLModel, table=True, extend_existing=True):
    """
    Represents the configuration for AI provider selection, including base_url, API key, and provider type
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    provider_type: str = Field(description="The type of AI provider (e.g., 'groq', 'openai', 'openrouter', 'cohere')")
    base_url: str = Field(description="The base URL for the AI provider API")
    api_key: str = Field(description="The API key for authenticating with the provider")
    model_name: str = Field(default="llama3-70b-8192", description="The specific model to use (e.g., 'llama3-70b-8192')")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    fallback_enabled: bool = Field(default=False, description="Whether fallback providers are enabled")
    fallback_base_url: Optional[str] = Field(default=None, description="Base URL for fallback provider")
    fallback_api_key: Optional[str] = Field(default=None, description="API key for fallback provider")