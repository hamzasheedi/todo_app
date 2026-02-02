"""
AI Provider Factory
Creates and manages AI provider instances based on configuration
"""

from openai import OpenAI
from typing import Optional
from ..config.ai_settings import AISettings
import logging

logger = logging.getLogger(__name__)


class AIProviderFactory:
    """Factory class to create and manage AI provider instances"""

    @staticmethod
    def create_primary_client() -> OpenAI:
        """Create a client for the primary AI provider"""
        # Validate configuration before creating client
        AISettings.validate_configuration()

        logger.info(f"Initializing AI provider: {AISettings.AI_PROVIDER}")
        logger.info(f"Using base URL: {AISettings.AI_BASE_URL}")
        logger.info(f"Using model: {AISettings.AI_MODEL}")

        return OpenAI(
            base_url=AISettings.AI_BASE_URL,
            api_key=AISettings.AI_API_KEY,
        )

    @staticmethod
    def create_fallback_client() -> Optional[OpenAI]:
        """Create a client for the fallback AI provider if configured"""
        if AISettings.FALLBACK_AI_BASE_URL and AISettings.FALLBACK_AI_API_KEY:
            logger.info("Initializing fallback AI provider")
            return OpenAI(
                base_url=AISettings.FALLBACK_AI_BASE_URL,
                api_key=AISettings.FALLBACK_AI_API_KEY,
            )
        logger.info("No fallback AI provider configured")
        return None

    @staticmethod
    def get_current_provider_info():
        """Get information about the currently configured provider"""
        return {
            "primary_provider": AISettings.AI_PROVIDER,
            "primary_base_url": AISettings.AI_BASE_URL,
            "model": AISettings.AI_MODEL,
            "has_fallback": bool(AISettings.FALLBACK_AI_BASE_URL and AISettings.FALLBACK_AI_API_KEY)
        }