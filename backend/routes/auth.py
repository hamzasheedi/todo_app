from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Optional
from ..database.database import SessionLocal
from ..models.user import User
from ..schemas.user import UserCreate, UserRead
from ..auth.jwt import SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import datetime, timedelta
import uuid
from passlib.context import CryptContext

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create router
router = APIRouter(prefix="/api/auth", tags=["auth"])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a plain password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default 15 minutes

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/signup", response_model=UserRead)
def register_user(user_data: UserCreate, session: Session = Depends(SessionLocal)):
    """Register a new user"""
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user_data.password)

    # Create new user with hashed password
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@router.post("/signin")
def login_user(user_data: UserCreate, session: Session = Depends(SessionLocal)):
    """Login a user and return JWT token"""
    # Find user by email
    user = session.exec(select(User).where(User.email == user_data.email)).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)  # 30 minutes
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signout")
def logout_user():
    """Logout a user"""
    # In a stateless JWT system, the server doesn't store session information
    # So this endpoint is more for client-side cleanup
    return {"message": "Successfully logged out"}