from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging
import traceback
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorDetail:
    """
    Standardized error detail structure
    """
    def __init__(self, code: str, message: str, field: str = None, location: str = None):
        self.code = code
        self.message = message
        self.field = field
        self.location = location

    def to_dict(self):
        result = {
            'code': self.code,
            'message': self.message
        }
        if self.field:
            result['field'] = self.field
        if self.location:
            result['location'] = self.location
        return result

class CustomException(HTTPException):
    """
    Custom exception with additional error details
    """
    def __init__(self, status_code: int, error_code: str, message: str, details: list = None):
        super().__init__(status_code=status_code, detail=message)
        self.error_code = error_code
        self.message = message
        self.details = details or []

    def to_dict(self):
        return {
            'error_code': self.error_code,
            'message': self.message,
            'details': [detail.to_dict() for detail in self.details],
            'timestamp': datetime.utcnow().isoformat()
        }

async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for the application
    """
    # Log the error with full traceback
    logger.error(f"Global exception: {str(exc)}", exc_info=True)

    # Determine the appropriate status code and error code
    if isinstance(exc, HTTPException):
        status_code = exc.status_code
        error_code = "HTTP_ERROR"
        message = exc.detail
    elif isinstance(exc, CustomException):
        status_code = exc.status_code
        error_code = exc.error_code
        message = exc.message
    else:
        status_code = 500
        error_code = "INTERNAL_ERROR"
        message = "An unexpected error occurred"

    # Create error response
    error_response = {
        'error_code': error_code,
        'message': message,
        'timestamp': datetime.utcnow().isoformat(),
        'path': str(request.url),
        'method': request.method
    }

    # Add more details for development environment
    if status_code == 500:
        error_response['debug'] = {
            'type': type(exc).__name__,
            'traceback': traceback.format_exc()
        }

    return JSONResponse(
        status_code=status_code,
        content=error_response
    )

async def validation_exception_handler(request: Request, exc: Exception):
    """
    Handler for validation errors
    """
    logger.warning(f"Validation error: {str(exc)}")

    error_details = []

    # Handle Pydantic validation errors
    if hasattr(exc, 'errors'):
        for error in exc.errors():
            field = ".".join(error['loc']) if error['loc'] else 'unknown'
            error_details.append({
                'code': error['type'],
                'message': error['msg'],
                'field': field
            })

    error_response = {
        'error_code': 'VALIDATION_ERROR',
        'message': 'Validation failed',
        'details': error_details,
        'timestamp': datetime.utcnow().isoformat(),
        'path': str(request.url),
        'method': request.method
    }

    return JSONResponse(
        status_code=422,
        content=error_response
    )

class ErrorHandler:
    """
    Centralized error handling utilities
    """

    @staticmethod
    def handle_database_error(exc: Exception, operation: str = "database operation"):
        """
        Handle database-specific errors
        """
        logger.error(f"Database error during {operation}: {str(exc)}")

        if "duplicate key" in str(exc).lower():
            raise CustomException(
                status_code=409,
                error_code="DUPLICATE_ENTRY",
                message="A record with this identifier already exists"
            )
        elif "foreign key" in str(exc).lower():
            raise CustomException(
                status_code=400,
                error_code="FOREIGN_KEY_VIOLATION",
                message="Referenced record does not exist"
            )
        else:
            raise CustomException(
                status_code=500,
                error_code="DATABASE_ERROR",
                message=f"Database error occurred during {operation}"
            )

    @staticmethod
    def handle_auth_error(exc: Exception, operation: str = "authentication"):
        """
        Handle authentication-specific errors
        """
        logger.warning(f"Auth error during {operation}: {str(exc)}")

        raise CustomException(
            status_code=401,
            error_code="AUTHENTICATION_ERROR",
            message="Authentication failed"
        )

    @staticmethod
    def handle_permission_error(resource: str = "resource"):
        """
        Handle permission-specific errors
        """
        logger.warning(f"Permission error: Access denied to {resource}")

        raise CustomException(
            status_code=403,
            error_code="PERMISSION_DENIED",
            message=f"Access denied to {resource}"
        )

    @staticmethod
    def handle_not_found_error(resource: str, resource_id: str = None):
        """
        Handle not found errors
        """
        message = f"{resource} not found"
        if resource_id:
            message = f"{resource} with ID {resource_id} not found"

        logger.info(f"Not found error: {message}")

        raise CustomException(
            status_code=404,
            error_code="NOT_FOUND",
            message=message
        )

# Standardized error responses
STANDARD_ERRORS = {
    400: {
        'error_code': 'BAD_REQUEST',
        'message': 'The request was invalid or cannot be served'
    },
    401: {
        'error_code': 'UNAUTHORIZED',
        'message': 'Authentication is required or has failed'
    },
    403: {
        'error_code': 'FORBIDDEN',
        'message': 'Access to the requested resource is forbidden'
    },
    404: {
        'error_code': 'NOT_FOUND',
        'message': 'The requested resource could not be found'
    },
    409: {
        'error_code': 'CONFLICT',
        'message': 'The request could not be completed due to a conflict'
    },
    422: {
        'error_code': 'UNPROCESSABLE_ENTITY',
        'message': 'The request was well-formed but was unable to be followed due to semantic errors'
    },
    500: {
        'error_code': 'INTERNAL_ERROR',
        'message': 'An internal server error occurred'
    }
}