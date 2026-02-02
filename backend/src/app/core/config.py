import os
from typing import Optional
from pydantic import BaseModel
import dotenv

dotenv.load_dotenv()


class AIConfig(BaseModel):
    """Configuration for AI integration"""
    gemini_api_key: str
    gemini_base_url: str
    model_name: str = "gemini-2.0-flash"  # Default model


def get_ai_config() -> AIConfig:
    """Get AI configuration from environment variables"""
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable is required")

    # Default to Google's Gemini API base URL, but allow override
    gemini_base_url = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta")

    model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.0-flash")

    return AIConfig(
        gemini_api_key=gemini_api_key,
        gemini_base_url=gemini_base_url,
        model_name=model_name
    )