"""
AI Validation Service
Validates AI provider configuration and requests
"""

import os
from typing import Dict, Any
from ..config.ai_settings import AISettings
from ..services.validation import ValidationService


class AIValidationService:
    """Service class for validating AI provider configuration and requests"""
    
    @staticmethod
    def validate_ai_provider_configuration() -> Dict[str, Any]:
        """Validate that the AI provider is properly configured"""
        errors = []
        
        # Check that required environment variables are set
        if not AISettings.AI_API_KEY:
            errors.append("AI_API_KEY environment variable is not set")
        
        if not AISettings.AI_BASE_URL:
            errors.append("AI_BASE_URL environment variable is not set")
        
        if not AISettings.AI_MODEL:
            errors.append("AI_MODEL environment variable is not set")
        
        # Check that the provider type is valid
        valid_providers = ["groq", "openai", "openrouter", "cohere"]
        if AISettings.AI_PROVIDER not in valid_providers:
            errors.append(f"AI_PROVIDER must be one of {valid_providers}, got: {AISettings.AI_PROVIDER}")
        
        # Check if fallback is configured properly if enabled
        if AISettings.FALLBACK_AI_BASE_URL or AISettings.FALLBACK_AI_API_KEY:
            if not AISettings.FALLBACK_AI_BASE_URL:
                errors.append("FALLBACK_AI_BASE_URL must be set if fallback is partially configured")
            if not AISettings.FALLBACK_AI_API_KEY:
                errors.append("FALLBACK_AI_API_KEY must be set if fallback is partially configured")
        
        if errors:
            return {
                "valid": False,
                "errors": errors
            }
        else:
            return {
                "valid": True,
                "provider": AISettings.AI_PROVIDER,
                "model": AISettings.AI_MODEL
            }
    
    @staticmethod
    def validate_ai_request(user_input: str) -> Dict[str, Any]:
        """Validate an incoming AI request"""
        return ValidationService.validate_ai_request(user_input)
    
    @staticmethod
    def validate_mcp_tool_parameters(tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate parameters for MCP tool execution"""
        return ValidationService.validate_mcp_tool_parameters(tool_name, parameters)