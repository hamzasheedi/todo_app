from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "incomplete"

class TaskCreate(TaskBase):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "incomplete"

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TaskComplete(BaseModel):
    status: str  # "complete" or "incomplete"

class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_date: datetime
    updated_date: datetime