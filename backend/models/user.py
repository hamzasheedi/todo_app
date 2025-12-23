from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)

class User(UserBase, table=True):
    """
    Represents a registered user of the system with authentication credentials
    """
    id: uuid.UUID = Field(default=None, primary_key=True, sa_column_kwargs={"nullable": False})
    email: str = Field(unique=True, nullable=False, max_length=255)
    better_auth_id: Optional[str] = Field(default=None, unique=True, nullable=True)  # Store Better Auth user ID
    created_date: datetime = Field(default=None, sa_column_kwargs={"nullable": False})
    updated_date: datetime = Field(default=None, sa_column_kwargs={"nullable": False})

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")