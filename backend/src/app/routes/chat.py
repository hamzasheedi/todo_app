from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
import uuid
from pydantic import BaseModel
from sqlmodel import Session, select
from datetime import datetime

# Import from app modules
from app.auth.backend_jwt import get_current_user_from_backend_jwt
from app.models.user import User
from app.models.task import Task
from app.database.database import get_session

router = APIRouter(tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    tool_results: Dict[str, Any] = None

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    current_user: User = Depends(get_current_user_from_backend_jwt),
    session: Session = Depends(get_session)
):
    """
    Main chat endpoint that processes natural language and interacts with tasks.
    This endpoint provides AI-powered task management capabilities.
    """
    try:
        message = request.message

        # Simple NLP to determine intent and parameters
        message_lower = message.lower()

        if any(word in message_lower for word in ["add", "create", "new", "task"]):
            # Extract task title from message
            words = message.split()
            title_start = None

            for i, word in enumerate(words):
                if word.lower() in ["add", "create", "new"]:
                    title_start = i + 1
                    break
                elif "task" in word.lower() and i > 0:
                    title_start = i + 1
                    break

            if title_start and title_start < len(words):
                task_title = " ".join(words[title_start:])
                # Clean up the title if it contains common phrases
                if "task" in task_title.lower():
                    task_title = task_title.lower().replace("task", "").strip()
                if "called" in task_title.lower():
                    task_title = task_title.lower().replace("called", "").strip()
                if "named" in task_title.lower():
                    task_title = task_title.lower().replace("named", "").strip()

                # Create the task
                new_task = Task(
                    id=uuid.uuid4(),
                    user_id=current_user.id,
                    title=task_title or "New task",
                    description=None,
                    status="incomplete",
                    created_date=datetime.utcnow(),
                    updated_date=datetime.utcnow()
                )

                session.add(new_task)
                session.commit()
                session.refresh(new_task)

                response_text = f"I've created the task: '{new_task.title}'"
                return ChatResponse(
                    response=response_text,
                    conversation_id=request.conversation_id or str(uuid.uuid4()),
                    tool_results={"task_created": str(new_task.id)}
                )

        elif any(word in message_lower for word in ["list", "show", "all", "my", "tasks"]):
            # Get user's tasks
            user_tasks = session.exec(
                select(Task).where(Task.user_id == current_user.id)
            ).all()

            if user_tasks:
                task_list = [f"- {task.title} ({task.status})" for task in user_tasks]
                response_text = f"Here are your tasks:\n" + "\n".join(task_list)
            else:
                response_text = "You don't have any tasks yet."

            return ChatResponse(
                response=response_text,
                conversation_id=request.conversation_id or str(uuid.uuid4()),
                tool_results={"tasks_count": len(user_tasks)}
            )

        elif any(word in message_lower for word in ["complete", "done", "finish", "mark"]):
            # Try to find a task that matches words in the message
            user_tasks = session.exec(
                select(Task).where(Task.user_id == current_user.id, Task.status == "incomplete")
            ).all()

            matched_task = None
            if user_tasks:
                for task in user_tasks:
                    if any(word in task.title.lower() for word in message_lower.split()):
                        matched_task = task
                        break

                # If no specific task found, use the most recent one
                if not matched_task and user_tasks:
                    matched_task = user_tasks[0]

            if matched_task:
                # Mark task as complete
                matched_task.status = "complete"
                matched_task.updated_date = datetime.utcnow()
                session.add(matched_task)
                session.commit()
                session.refresh(matched_task)

                response_text = f"I've marked the task '{matched_task.title}' as complete!"
            else:
                response_text = "I couldn't find a task to complete. Could you please specify which task you'd like to mark as complete?"

            return ChatResponse(
                response=response_text,
                conversation_id=request.conversation_id or str(uuid.uuid4()),
                tool_results={"task_completed": str(matched_task.id) if matched_task else None}
            )

        else:
            # Default response for unrecognized commands
            response_text = "I can help you manage your tasks. You can ask me to add, list, show, update, complete, or delete tasks. For example: 'Add a task to buy groceries' or 'Show me my tasks'."
            return ChatResponse(
                response=response_text,
                conversation_id=request.conversation_id or str(uuid.uuid4()),
                tool_results=None
            )

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )