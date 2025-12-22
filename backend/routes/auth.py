from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Optional
import uuid
from pydantic import BaseModel

# Handle relative imports for different execution contexts
try:
    from ..database.database import SessionLocal
    from ..models.user import User
    from ..schemas.user import UserCreate, UserRead
    from ..auth.jwt import get_current_user
    from ..auth.backend_jwt import create_backend_jwt, get_current_user_from_backend_jwt
except ImportError:
    # Direct imports for test environments
    from database.database import SessionLocal
    from models.user import User
    from schemas.user import UserCreate, UserRead
    from auth.jwt import get_current_user
    from auth.backend_jwt import create_backend_jwt, get_current_user_from_backend_jwt

# Create router
router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.get("/me")
def get_authenticated_user(current_user: User = Depends(get_current_user_from_backend_jwt)):
    """Get the authenticated user's information including backend ID"""
    return {
        "id": str(current_user.id),  # Backend UUID
        "email": current_user.email,
        "better_auth_id": current_user.better_auth_id,  # Better Auth ID if available
        "created_date": current_user.created_date,
        "updated_date": current_user.updated_date
    }

from pydantic import BaseModel

class SyncUserRequest(BaseModel):
    better_auth_id: str
    email: str

@router.post("/sync-user")
def sync_user_with_backend(
    sync_data: SyncUserRequest,
    session: Session = Depends(SessionLocal)
):
    """Sync a Better Auth user with the backend database and return backend JWT"""
    better_auth_id = sync_data.better_auth_id
    email = sync_data.email

    if not better_auth_id or not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="better_auth_id and email are required"
        )

    # Check if user already exists with this Better Auth ID
    existing_user = session.exec(select(User).where(User.better_auth_id == better_auth_id)).first()

    if existing_user:
        # User already exists, return existing user with backend JWT
        backend_token = create_backend_jwt(str(existing_user.id), existing_user.email, existing_user.better_auth_id)
        return {
            "id": str(existing_user.id),
            "email": existing_user.email,
            "better_auth_id": existing_user.better_auth_id,
            "backend_token": backend_token,  # Add backend JWT for API calls
            "message": "User already exists"
        }

    # Check if user exists with this email but no Better Auth ID
    existing_user_by_email = session.exec(select(User).where(
        User.email == email
    )).first()

    if existing_user_by_email:
        # Update existing user with Better Auth ID
        existing_user_by_email.better_auth_id = better_auth_id
        from datetime import datetime
        existing_user_by_email.updated_date = datetime.utcnow()  # Update the timestamp
        session.add(existing_user_by_email)
        session.commit()
        session.refresh(existing_user_by_email)

        backend_token = create_backend_jwt(str(existing_user_by_email.id), existing_user_by_email.email, existing_user_by_email.better_auth_id)
        return {
            "id": str(existing_user_by_email.id),
            "email": existing_user_by_email.email,
            "better_auth_id": existing_user_by_email.better_auth_id,
            "backend_token": backend_token,  # Add backend JWT for API calls
            "message": "User updated with Better Auth ID"
        }

    import uuid
    from datetime import datetime
    # Create new user with Better Auth ID and set all required fields manually
    new_user = User(
        id=uuid.uuid4(),
        email=email,
        better_auth_id=better_auth_id,
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    backend_token = create_backend_jwt(str(new_user.id), new_user.email, new_user.better_auth_id)
    return {
        "id": str(new_user.id),
        "email": new_user.email,
        "better_auth_id": new_user.better_auth_id,
        "backend_token": backend_token,  # Add backend JWT for API calls
        "message": "User created successfully"
    }

@router.post("/get-backend-token")
def get_backend_token(
    session: Session = Depends(SessionLocal)
):
    """
    Get a backend-specific JWT after user has been synced
    This endpoint should be called after successful user sync
    """
    # Since this endpoint will be called after sync, we can't verify the original token
    # Instead, we'll require the client to send user identification that was established during sync
    # For security, we'll implement this as a separate flow that requires user verification through sync first
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This endpoint requires special implementation for secure token exchange"
    )


@router.post("/signout")
def logout_user():
    """Logout a user"""
    # In a stateless JWT system, the server doesn't store session information
    # So this endpoint is more for client-side cleanup
    return {"message": "Successfully logged out"}