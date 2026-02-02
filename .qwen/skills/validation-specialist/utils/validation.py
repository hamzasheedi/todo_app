from typing import Any, Dict, List
from pydantic import BaseModel, validator, ValidationError
import re
from datetime import datetime

class ValidationUtils:
    """
    Comprehensive validation utilities for the Todo application
    """

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format using regex
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """
        Validate password strength and return validation results
        """
        validation_result = {
            'is_valid': True,
            'errors': [],
            'strength_score': 0
        }

        # Check minimum length
        if len(password) < 8:
            validation_result['is_valid'] = False
            validation_result['errors'].append('Password must be at least 8 characters')

        # Check for uppercase
        if not re.search(r'[A-Z]', password):
            validation_result['is_valid'] = False
            validation_result['errors'].append('Password must contain uppercase letter')

        # Check for lowercase
        if not re.search(r'[a-z]', password):
            validation_result['is_valid'] = False
            validation_result['errors'].append('Password must contain lowercase letter')

        # Check for digit
        if not re.search(r'\d', password):
            validation_result['is_valid'] = False
            validation_result['errors'].append('Password must contain a digit')

        # Calculate strength score
        score = 0
        if len(password) >= 8: score += 1
        if re.search(r'[A-Z]', password): score += 1
        if re.search(r'[a-z]', password): score += 1
        if re.search(r'\d', password): score += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): score += 1

        validation_result['strength_score'] = score
        return validation_result

    @staticmethod
    def validate_task_title(title: str) -> Dict[str, Any]:
        """
        Validate task title according to specification (1-200 characters)
        """
        validation_result = {
            'is_valid': True,
            'errors': []
        }

        if not title or len(title.strip()) == 0:
            validation_result['is_valid'] = False
            validation_result['errors'].append('Task title is required')
        elif len(title) > 200:
            validation_result['is_valid'] = False
            validation_result['errors'].append('Task title must be 200 characters or less')

        return validation_result

    @staticmethod
    def validate_task_description(description: str) -> Dict[str, Any]:
        """
        Validate task description according to specification (0-1000 characters)
        """
        validation_result = {
            'is_valid': True,
            'errors': []
        }

        if description and len(description) > 1000:
            validation_result['is_valid'] = False
            validation_result['errors'].append('Task description must be 1000 characters or less')

        return validation_result

    @staticmethod
    def validate_user_id(user_id: str) -> Dict[str, Any]:
        """
        Validate user ID format (UUID)
        """
        validation_result = {
            'is_valid': True,
            'errors': []
        }

        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        if not re.match(uuid_pattern, user_id):
            validation_result['is_valid'] = False
            validation_result['errors'].append('Invalid user ID format')

        return validation_result

class TaskValidationSchema(BaseModel):
    """
    Pydantic schema for task validation
    """
    title: str
    description: str = ""
    status: str = "incomplete"

    @validator('title')
    def validate_title(cls, v):
        result = ValidationUtils.validate_task_title(v)
        if not result['is_valid']:
            raise ValueError(result['errors'][0])
        return v.strip()

    @validator('description')
    def validate_description(cls, v):
        result = ValidationUtils.validate_task_description(v)
        if not result['is_valid']:
            raise ValueError(result['errors'][0])
        return v

    @validator('status')
    def validate_status(cls, v):
        if v not in ['incomplete', 'complete']:
            raise ValueError('Status must be either "incomplete" or "complete"')
        return v

class UserValidationSchema(BaseModel):
    """
    Pydantic schema for user validation
    """
    email: str
    password: str

    @validator('email')
    def validate_email(cls, v):
        if not ValidationUtils.validate_email(v):
            raise ValueError('Invalid email format')
        return v.lower()

    @validator('password')
    def validate_password(cls, v):
        result = ValidationUtils.validate_password_strength(v)
        if not result['is_valid']:
            raise ValueError('; '.join(result['errors']))
        return v