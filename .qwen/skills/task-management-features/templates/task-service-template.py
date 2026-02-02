from typing import List, Optional
from sqlmodel import Session, select
from backend.models import Task
from backend.schemas import TaskCreate, TaskUpdate, TaskRead
from backend.utils.validation import ValidationUtils
from backend.utils.error_handlers import ErrorHandler

class TaskService:
    """
    Comprehensive task management service with all CRUD operations and business logic
    """

    def __init__(self, db_session: Session):
        self.db = db_session

    def create_task(self, user_id: str, task_data: TaskCreate) -> TaskRead:
        """
        Create a new task for the specified user
        """
        # Validate input data
        title_validation = ValidationUtils.validate_task_title(task_data.title)
        if not title_validation['is_valid']:
            raise ValueError('; '.join(title_validation['errors']))

        description_validation = ValidationUtils.validate_task_description(task_data.description)
        if not description_validation['is_valid']:
            raise ValueError('; '.join(description_validation['errors']))

        # Create task instance
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status or "incomplete",
            user_id=user_id
        )

        # Add to database
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return TaskRead.from_orm(task)

    def get_task(self, task_id: str, user_id: str) -> Optional[TaskRead]:
        """
        Get a specific task by ID for the specified user
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = self.db.exec(statement).first()

        if not task:
            ErrorHandler.handle_not_found_error("Task", task_id)

        return TaskRead.from_orm(task) if task else None

    def get_tasks(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        sort_by: str = "created_date",
        sort_order: str = "desc"
    ) -> List[TaskRead]:
        """
        Get all tasks for the specified user with filtering and sorting
        """
        statement = select(Task).where(Task.user_id == user_id)

        # Apply status filter if provided
        if status:
            statement = statement.where(Task.status == status)

        # Apply sorting
        if sort_by == "title":
            if sort_order == "asc":
                statement = statement.order_by(Task.title.asc())
            else:
                statement = statement.order_by(Task.title.desc())
        elif sort_by == "created_date":
            if sort_order == "asc":
                statement = statement.order_by(Task.created_date.asc())
            else:
                statement = statement.order_by(Task.created_date.desc())
        elif sort_by == "updated_date":
            if sort_order == "asc":
                statement = statement.order_by(Task.updated_date.asc())
            else:
                statement = statement.order_by(Task.updated_date.desc())
        elif sort_by == "status":
            if sort_order == "asc":
                statement = statement.order_by(Task.status.asc())
            else:
                statement = statement.order_by(Task.status.desc())

        # Apply pagination
        statement = statement.offset(skip).limit(limit)
        tasks = self.db.exec(statement).all()

        return [TaskRead.from_orm(task) for task in tasks]

    def update_task(self, task_id: str, user_id: str, task_data: TaskUpdate) -> TaskRead:
        """
        Update an existing task
        """
        # Get the existing task
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = self.db.exec(statement).first()

        if not task:
            ErrorHandler.handle_not_found_error("Task", task_id)

        # Update fields if provided
        if task_data.title is not None:
            title_validation = ValidationUtils.validate_task_title(task_data.title)
            if not title_validation['is_valid']:
                raise ValueError('; '.join(title_validation['errors']))
            task.title = task_data.title

        if task_data.description is not None:
            description_validation = ValidationUtils.validate_task_description(task_data.description)
            if not description_validation['is_valid']:
                raise ValueError('; '.join(description_validation['errors']))
            task.description = task_data.description

        if task_data.status is not None:
            if task_data.status not in ["incomplete", "complete"]:
                raise ValueError("Status must be either 'incomplete' or 'complete'")
            task.status = task_data.status

        # Update the updated_date
        from datetime import datetime
        task.updated_date = datetime.utcnow()

        # Commit changes
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return TaskRead.from_orm(task)

    def delete_task(self, task_id: str, user_id: str) -> bool:
        """
        Delete a task
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = self.db.exec(statement).first()

        if not task:
            ErrorHandler.handle_not_found_error("Task", task_id)

        self.db.delete(task)
        self.db.commit()

        return True

    def update_task_status(self, task_id: str, user_id: str, status: str) -> TaskRead:
        """
        Update only the status of a task
        """
        if status not in ["incomplete", "complete"]:
            raise ValueError("Status must be either 'incomplete' or 'complete'")

        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = self.db.exec(statement).first()

        if not task:
            ErrorHandler.handle_not_found_error("Task", task_id)

        task.status = status
        from datetime import datetime
        task.updated_date = datetime.utcnow()

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return TaskRead.from_orm(task)

    def get_task_statistics(self, user_id: str) -> dict:
        """
        Get task statistics for the user
        """
        all_tasks_statement = select(Task).where(Task.user_id == user_id)
        all_tasks = self.db.exec(all_tasks_statement).all()

        total_tasks = len(all_tasks)
        completed_tasks = len([task for task in all_tasks if task.status == "complete"])
        incomplete_tasks = total_tasks - completed_tasks

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "incomplete_tasks": incomplete_tasks,
            "completion_rate": completed_tasks / total_tasks if total_tasks > 0 else 0
        }