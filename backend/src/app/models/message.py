from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class MessageBase(SQLModel):
    content: str = Field(min_length=1, max_length=500)
    role: str = Field(max_length=20)  # 'user' or 'assistant'

class Message(MessageBase, table=True, extend_existing=True):
    """
    Represents a message in a conversation
    """
    id: uuid.UUID = Field(default=None, primary_key=True, sa_column_kwargs={"nullable": False})
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", nullable=False)
    content: str = Field(min_length=1, max_length=500)
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    timestamp: datetime = Field(default=None, sa_column_kwargs={"nullable": False})

    # Relationship to conversation
    # conversation: Optional["Conversation"] = Relationship(back_populates="messages")