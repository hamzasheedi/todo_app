from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: str = Field(default="incomplete", regex="^(incomplete|complete)$")

class Task(TaskBase, table=True):
    """
    Represents a single todo item owned by a specific user
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: str = Field(default="incomplete", regex="^(incomplete|complete)$")
    created_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")

    # Update the updated_date field automatically
    def __setattr__(self, name, value):
        if name == 'updated_date':
            super().__setattr__(name, datetime.utcnow())
        else:
            super().__setattr__(name, value)