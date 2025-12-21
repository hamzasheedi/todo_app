from fastapi import HTTPException, status
from typing import Union
import uuid
from ..models.user import User

def validate_uuid(value: str) -> uuid.UUID:
    """
    Validate that a string is a valid UUID
    """
    try:
        return uuid.UUID(value)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid UUID format: {value}"
        )

def validate_user_id_match(token_user_id: Union[str, uuid.UUID], url_user_id: Union[str, uuid.UUID]) -> bool:
    """
    Validate that the user ID in the JWT token matches the user ID in the URL parameter
    This is critical for user isolation and security
    """
    # Convert to UUID if they're strings
    if isinstance(token_user_id, str):
        token_user_id = uuid.UUID(token_user_id)
    if isinstance(url_user_id, str):
        url_user_id = uuid.UUID(url_user_id)

    # Compare the UUIDs
    if token_user_id != url_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID in token does not match user ID in URL"
        )

    return True

def validate_task_ownership(current_user: User, task_user_id: uuid.UUID) -> bool:
    """
    Validate that the current user owns the task they're trying to access
    """
    if current_user.id != task_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You do not own this task"
        )

    return True