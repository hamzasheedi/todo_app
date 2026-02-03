"""
AI Settings Configuration
Handles environment variables for AI provider configuration
"""

import os
from typing import Optional


class AISettings:
    """Configuration class for AI provider settings"""

    # Determine which provider to use based on environment
    # Prioritize Groq if AI_PROVIDER is set to "groq" or if GROQ_API_KEY is set
    # Otherwise use Gemini if GEMINI_API_KEY is set
    AI_PROVIDER_CHOICE: str = os.getenv("AI_PROVIDER", "groq")
    HAS_GROQ_CONFIG = bool(os.getenv("AI_API_KEY"))  # Using the generic AI_API_KEY for Groq
    HAS_GEMINI_CONFIG = bool(os.getenv("GEMINI_API_KEY"))

    if AI_PROVIDER_CHOICE.lower() == "groq" and HAS_GROQ_CONFIG:
        # Use Groq as the primary provider
        AI_PROVIDER: str = "groq"
        AI_BASE_URL: str = os.getenv("AI_BASE_URL", "https://api.groq.com/openai/v1")
        AI_API_KEY: str = os.getenv("AI_API_KEY", "")
        AI_MODEL: str = os.getenv("AI_MODEL", "llama3-70b-8192")
    elif HAS_GEMINI_CONFIG:
        # Use Google Gemini as the fallback provider
        AI_PROVIDER: str = "gemini"
        AI_BASE_URL: str = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai")
        AI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
        AI_MODEL: str = os.getenv("GEMINI_MODEL_NAME", "gemini-2.0-flash")
    else:
        # Default to Groq if no specific configuration is found
        AI_PROVIDER: str = "groq"
        AI_BASE_URL: str = os.getenv("AI_BASE_URL", "https://api.groq.com/openai/v1")
        AI_API_KEY: str = os.getenv("AI_API_KEY", "")
        AI_MODEL: str = os.getenv("AI_MODEL", "llama3-70b-8192")

    AI_TIMEOUT: int = int(os.getenv("AI_TIMEOUT", "60"))  # Increased to 60 seconds to allow for tool calling cycles

    # Fallback provider settings
    FALLBACK_AI_BASE_URL: Optional[str] = os.getenv("FALLBACK_AI_BASE_URL")
    FALLBACK_AI_API_KEY: Optional[str] = os.getenv("FALLBACK_AI_API_KEY")

    # Validation
    @classmethod
    def validate_configuration(cls) -> bool:
        """Validate that required AI configuration is present"""
        if not cls.AI_API_KEY:
            raise ValueError(f"{cls.AI_PROVIDER.upper()}_API_KEY environment variable is required")

        if not cls.AI_BASE_URL:
            raise ValueError(f"{cls.AI_PROVIDER.upper()}_BASE_URL environment variable is required")

        return True