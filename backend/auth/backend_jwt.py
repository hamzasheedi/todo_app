from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional
import os
from dotenv import load_dotenv

# Handle relative imports for different execution contexts
try:
    from ..models.user import User
    from ..database.database import get_session
except ImportError:
    # Direct imports for test environments
    from models.user import User
    from database.database import get_session

from sqlmodel import Session, select
import uuid
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Initialize security scheme
security = HTTPBearer()

# Get backend JWT secret (separate from Better Auth secret)
BACKEND_JWT_SECRET = os.getenv("JWT_SECRET", "fallback-jwt-secret-change-in-production")
BACKEND_JWT_ALGORITHM = "HS256"

def create_backend_jwt(user_id: str, email: str, better_auth_id: Optional[str] = None) -> str:
    """
    Create a backend-specific JWT for API authentication
    """
    expire = datetime.utcnow() + timedelta(days=7)  # Token expires in 7 days
    to_encode = {
        "sub": user_id,
        "email": email,
        "better_auth_id": better_auth_id,
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp()
    }
    encoded_jwt = jwt.encode(to_encode, BACKEND_JWT_SECRET, algorithm=BACKEND_JWT_ALGORITHM)
    return encoded_jwt

def verify_backend_jwt(token: str) -> dict:
    """
    Verify backend-specific JWT and return payload
    """
    try:
        payload = jwt.decode(token, BACKEND_JWT_SECRET, algorithms=[BACKEND_JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user_from_backend_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Get current user from backend JWT
    """
    token = credentials.credentials
    payload = verify_backend_jwt(token)

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - no user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Find user by their backend UUID
    user = session.exec(select(User).where(User.id == uuid.UUID(user_id))).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user