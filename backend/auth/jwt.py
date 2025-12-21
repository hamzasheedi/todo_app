from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional
import os
from dotenv import load_dotenv
from ..models.user import User
from ..database.database import get_session
from sqlmodel import Session, select
import uuid

# Load environment variables
load_dotenv()

# Initialize security scheme
security = HTTPBearer()

# Get JWT secret from environment
SECRET_KEY = os.getenv("JWT_SECRET", "your-default-jwt-secret-key-change-in-production")
ALGORITHM = "HS256"

def verify_token(token: str) -> dict:
    """
    Verify JWT token and return payload
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Get current user from JWT token
    """
    token = credentials.credentials
    payload = verify_token(token)
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convert user_id to UUID if it's a string representation
    try:
        user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Query the user from the database
    user = session.exec(select(User).where(User.id == user_uuid)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user