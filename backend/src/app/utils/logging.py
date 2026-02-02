"""
Logging Configuration
Sets up logging for AI provider configuration and other services
"""

import logging
import sys
from logging.handlers import RotatingFileHandler


def setup_logging():
    """Set up logging configuration for the application"""
    
    # Create a custom logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Create formatters and add it to handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # Add handlers to the logger
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    # Also add file handler for detailed logging
    file_handler = RotatingFileHandler(
        'app.log', maxBytes=1024*1024*5, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Prevent duplicate logs
    logger.propagate = False
    
    return logger


# Set up logging when module is imported
app_logger = setup_logging()


def log_ai_provider_config():
    """Log the AI provider configuration at startup"""
    from .config.ai_settings import AISettings
    
    app_logger.info("=== AI Provider Configuration ===")
    app_logger.info(f"Provider: {AISettings.AI_PROVIDER}")
    app_logger.info(f"Base URL: {AISettings.AI_BASE_URL}")
    app_logger.info(f"Model: {AISettings.AI_MODEL}")
    app_logger.info(f"Has Fallback: {bool(AISettings.FALLBACK_AI_BASE_URL and AISettings.FALLBACK_AI_API_KEY)}")
    app_logger.info("===============================")