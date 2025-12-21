from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)

class User(UserBase, table=True):
    """
    Represents a registered user of the system with authentication credentials
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    created_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Update the updated_date field automatically
    def __setattr__(self, name, value):
        if name == 'updated_date':
            super().__setattr__(name, datetime.utcnow())
        else:
            super().__setattr__(name, value)