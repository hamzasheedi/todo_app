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
    id: uuid.UUID = Field(default=None, primary_key=True, sa_column_kwargs={"nullable": False})
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: str = Field(default="incomplete", regex="^(incomplete|complete)$")
    created_date: datetime = Field(default=None, sa_column_kwargs={"nullable": False})
    updated_date: datetime = Field(default=None, sa_column_kwargs={"nullable": False})

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")