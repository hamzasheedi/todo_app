from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
import uuid
from ..database.database import SessionLocal
from ..models.user import User
from ..models.task import Task
from ..schemas.task import TaskRead, TaskCreate, TaskUpdate, TaskComplete
from ..auth.jwt import get_current_user
from ..utils.validation import validate_uuid, validate_user_id_match, validate_task_ownership

# Create router with user_id in the path
router = APIRouter(tags=["tasks"])

@router.get("/{user_id}/tasks", response_model=List[TaskRead])
def get_user_tasks(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(SessionLocal),
    sort: Optional[str] = Query(None, description="Sort options: newest_first, oldest_first, highest_priority, lowest_priority")
):
    """Get all tasks for a specific user with optional sorting"""
    # Validate user_id format
    validated_user_id = validate_uuid(user_id)

    # Verify that the authenticated user matches the requested user_id
    validate_user_id_match(current_user.id, validated_user_id)

    # Build query for user's tasks
    query = select(Task).where(Task.user_id == validated_user_id)

    # Apply sorting based on parameter
    if sort == "newest_first":
        query = query.order_by(Task.created_date.desc())
    elif sort == "oldest_first":
        query = query.order_by(Task.created_date.asc())
    # Note: Priority sorting would require a priority field which is not in the current model

    tasks = session.exec(query).all()
    return tasks

@router.post("/{user_id}/tasks", response_model=TaskRead)
def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(SessionLocal)
):
    """Create a new task for the specified user"""
    # Validate user_id format
    validated_user_id = validate_uuid(user_id)

    # Verify that the authenticated user matches the requested user_id
    validate_user_id_match(current_user.id, validated_user_id)

    # Create new task
    db_task = Task(
        user_id=validated_user_id,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task

@router.get("/{user_id}/tasks/{task_id}", response_model=TaskRead)
def get_task(
    user_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(SessionLocal)
):
    """Get a specific task for the user"""
    # Validate both user_id and task_id formats
    validated_user_id = validate_uuid(user_id)
    validated_task_id = validate_uuid(task_id)

    # Verify that the authenticated user matches the requested user_id
    validate_user_id_match(current_user.id, validated_user_id)

    # Get the task
    task = session.exec(
        select(Task).where(Task.id == validated_task_id).where(Task.user_id == validated_user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify task ownership
    validate_task_ownership(current_user, task.user_id)

    return task

@router.put("/{user_id}/tasks/{task_id}", response_model=TaskRead)
def update_task(
    user_id: str,
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(SessionLocal)
):
    """Update a specific task for the user"""
    # Validate both user_id and task_id formats
    validated_user_id = validate_uuid(user_id)
    validated_task_id = validate_uuid(task_id)

    # Verify that the authenticated user matches the requested user_id
    validate_user_id_match(current_user.id, validated_user_id)

    # Get the existing task
    task = session.exec(
        select(Task).where(Task.id == validated_task_id).where(Task.user_id == validated_user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify task ownership
    validate_task_ownership(current_user, task.user_id)

    # Update task fields if provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.status is not None:
        task.status = task_data.status

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

@router.delete("/{user_id}/tasks/{task_id}")
def delete_task(
    user_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(SessionLocal)
):
    """Delete a specific task for the user"""
    # Validate both user_id and task_id formats
    validated_user_id = validate_uuid(user_id)
    validated_task_id = validate_uuid(task_id)

    # Verify that the authenticated user matches the requested user_id
    validate_user_id_match(current_user.id, validated_user_id)

    # Get the task to delete
    task = session.exec(
        select(Task).where(Task.id == validated_task_id).where(Task.user_id == validated_user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify task ownership
    validate_task_ownership(current_user, task.user_id)

    # Delete the task
    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}

@router.patch("/{user_id}/tasks/{task_id}/complete")
def update_task_completion(
    user_id: str,
    task_id: str,
    task_status: TaskComplete,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(SessionLocal)
):
    """Update the completion status of a specific task"""
    # Validate both user_id and task_id formats
    validated_user_id = validate_uuid(user_id)
    validated_task_id = validate_uuid(task_id)

    # Verify that the authenticated user matches the requested user_id
    validate_user_id_match(current_user.id, validated_user_id)

    # Get the task to update
    task = session.exec(
        select(Task).where(Task.id == validated_task_id).where(Task.user_id == validated_user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify task ownership
    validate_task_ownership(current_user, task.user_id)

    # Validate status
    if task_status.status not in ["complete", "incomplete"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be either 'complete' or 'incomplete'"
        )

    # Update task status
    task.status = task_status.status

    session.add(task)
    session.commit()
    session.refresh(task)

    # Create a proper TaskRead response
    task_read = TaskRead(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        status=task.status,
        created_date=task.created_date,
        updated_date=task.updated_date
    )

    return {"message": f"Task marked as {task_status.status}", "task": task_read}