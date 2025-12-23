from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    email: str
    password: str

class UserRead(UserBase):
    id: uuid.UUID
    created_date: datetime
    updated_date: datetime