from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)
    better_auth_id: Optional[str] = Field(default=None, max_length=255)  # Better Auth ID if available

class User(UserBase, table=True, extend_existing=True):
    """
    Represents a registered user of the system with authentication credentials
    """
    id: uuid.UUID = Field(default=None, primary_key=True, sa_column_kwargs={"nullable": False})
    email: str = Field(unique=True, nullable=False, max_length=255)
    better_auth_id: Optional[str] = Field(default=None, max_length=255)  # Better Auth ID if available
    created_at: datetime = Field(default=None, sa_column_kwargs={"nullable": False})
    updated_at: datetime = Field(default=None, sa_column_kwargs={"nullable": False})

    # Relationships to tasks and conversations
    tasks: List["Task"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "select"})
    conversations: List["Conversation"] = Relationship(back_populates="user", cascade_delete=True, sa_relationship_kwargs={"lazy": "select"})