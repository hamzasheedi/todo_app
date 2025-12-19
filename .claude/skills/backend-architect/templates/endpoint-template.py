from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session, select
from backend.models import Task
from backend.schemas import TaskRead, TaskCreate
from backend.database import get_session
from backend.auth.utils import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TaskRead])
def get_tasks(
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user
    """
    statement = select(Task).where(Task.user_id == current_user_id)
    tasks = session.exec(statement).all()
    return tasks

@router.post("/", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user
    """
    db_task = Task.from_orm(task)
    db_task.user_id = current_user_id
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task