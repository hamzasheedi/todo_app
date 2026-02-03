"""
Conversation Model
Represents a user's conversation with the AI, persisted in the database to maintain context across requests
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import uuid
from datetime import datetime
from sqlalchemy import JSON, Column


class Conversation(SQLModel, table=True, extend_existing=True):
    """
    Represents a user's conversation with the AI, persisted in the database to maintain context across requests
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: Optional[str] = Field(default=None, description="Title of the conversation")
    user_id: uuid.UUID = Field(foreign_key="user.id", description="Foreign key to the user who owns this conversation")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the conversation was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the conversation was last updated")
    messages: Optional[str] = Field(default=None, sa_column=Column(JSON), description="Array of messages in the conversation")
    extra_metadata: Optional[str] = Field(default=None, sa_column=Column(JSON), description="Additional metadata about the conversation")

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="conversations")