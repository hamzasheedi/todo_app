"""
Error Handler
Handles errors and creates appropriate responses
"""

import logging
from typing import Dict, Any
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)


class ErrorHandler:
    """Handles errors and creates appropriate responses"""
    
    @staticmethod
    def handle_provider_error(error: Exception, provider_name: str) -> Dict[str, Any]:
        """Handle errors from AI providers"""
        logger.error(f"Error from {provider_name} provider: {str(error)}")
        
        return {
            "error": f"Provider {provider_name} error",
            "message": str(error),
            "provider": provider_name
        }
    
    @staticmethod
    def handle_fallback_error(error: Exception) -> Dict[str, Any]:
        """Handle errors during fallback operations"""
        logger.error(f"Fallback error: {str(error)}")
        
        return {
            "error": "Fallback provider error",
            "message": "All providers are currently unavailable. Please try again later.",
        }
    
    @staticmethod
    def handle_validation_error(error: Exception) -> Dict[str, Any]:
        """Handle validation errors"""
        logger.warning(f"Validation error: {str(error)}")
        
        return {
            "error": "Validation error",
            "message": str(error)
        }
    
    @staticmethod
    def handle_general_error(error: Exception) -> Dict[str, Any]:
        """Handle general errors"""
        logger.error(f"General error: {str(error)}")
        
        return {
            "error": "Internal error",
            "message": "An internal error occurred. Please try again later."
        }


# Exception handlers for FastAPI
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions"""
    logger.warning(f"HTTP {exc.status_code} error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred"
        },
    )