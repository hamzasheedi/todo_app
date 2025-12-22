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

# Load environment variables
load_dotenv()

# Initialize security scheme
security = HTTPBearer()

# Get Better Auth secret from environment - should match the one used in frontend
SECRET_KEY = os.getenv("AUTH_SECRET", "fallback-secret-change-in-production")
ALGORITHM = "HS256"  # Better Auth typically uses HS256

def verify_token(token: str) -> dict:
    """
    Verify Better Auth token and return payload
    Better Auth can issue JWTs when properly configured
    """
    try:
        print(f"Token received for validation: {token[:20] if token else 'None'}...")  # Debug print
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No token provided",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Try decoding with various algorithms that Better Auth might use
        algorithms_to_try = ["HS256", "HS384", "HS512"]

        for algorithm in algorithms_to_try:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[algorithm])
                print(f"Successfully decoded JWT with {algorithm}: {payload}")
                return payload
            except JWTError:
                continue  # Try next algorithm

        # If all algorithms fail, this might not be a JWT
        print(f"Token could not be decoded as JWT with any algorithm: {token}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - invalid JWT",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        print(f"Token validation error: {e}")  # Debug print
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
    Get current user from Better Auth token
    """
    token = credentials.credentials
    payload = verify_token(token)

    print(f"Token payload: {payload}")  # Debug print

    # Handle different token formats
    better_auth_user_id = None

    # Try to extract user ID from various possible fields in the token
    if "token" in payload and "decoded" in payload:
        # This is a non-standard token, use the raw token value as the identifier
        better_auth_user_id = payload["token"]
    else:
        # This is a standard JWT, extract user ID normally
        better_auth_user_id = payload.get("sub") or payload.get("user_id") or payload.get("id") or payload.get("jti")

    print(f"Extracted user ID: {better_auth_user_id}")  # Debug print

    if better_auth_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - no user ID found in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # First, try to find the user by their Better Auth ID
    user = session.exec(select(User).where(User.better_auth_id == better_auth_user_id)).first()

    if user is None:
        # If not found, the user might not be synced yet
        # Let's also try to find by email if available in the token
        user_email = payload.get("email") if "email" in payload else None

        if user_email:
            user = session.exec(select(User).where(User.email == user_email)).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found in backend database. Please ensure user is properly registered.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # If we found the user by email, update the better_auth_id
        user.better_auth_id = better_auth_user_id
        session.add(user)
        session.commit()

    return user