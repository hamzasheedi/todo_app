"""
MCP Tool Registry
Manages registration and access to MCP tools for the AI agent
"""

from typing import Dict, Callable, Any, List
from .mcp_server import MCPServer
import logging


logger = logging.getLogger(__name__)


class ToolRegistry:
    """Registry for managing MCP tools available to the AI agent"""
    
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._tool_descriptions: Dict[str, str] = {}
        self._initialize_default_tools()
    
    def _initialize_default_tools(self):
        """Initialize default MCP tools"""
        # For now, we'll create placeholder methods that connect to the MCP server
        # Actual implementation would connect to the real MCP server
        self.register_tool(
            name="add_task",
            description="Add a new task to the user's task list",
            func=self._execute_add_task
        )
        
        self.register_tool(
            name="list_tasks",
            description="List all tasks for the user",
            func=self._execute_list_tasks
        )
        
        self.register_tool(
            name="update_task",
            description="Update an existing task",
            func=self._execute_update_task
        )
        
        self.register_tool(
            name="complete_task",
            description="Mark a task as completed",
            func=self._execute_complete_task
        )
        
        self.register_tool(
            name="delete_task",
            description="Delete a task from the user's list",
            func=self._execute_delete_task
        )
    
    def register_tool(self, name: str, description: str, func: Callable):
        """Register a new tool with the registry"""
        self._tools[name] = func
        self._tool_descriptions[name] = description
        logger.info(f"Registered tool: {name}")
    
    def get_tool(self, name: str) -> Callable:
        """Get a registered tool by name"""
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' is not registered")
        return self._tools[name]
    
    def get_tool_description(self, name: str) -> str:
        """Get the description of a registered tool"""
        return self._tool_descriptions.get(name, f"No description available for {name}")
    
    def list_available_tools(self) -> List[str]:
        """List all available tools"""
        return list(self._tools.keys())
    
    def execute_tool(self, name: str, session=None, **kwargs) -> Any:
        """Execute a tool with the given parameters"""
        tool = self.get_tool(name)
        logger.info(f"Executing tool: {name} with params: {kwargs}")
        try:
            # Remove any 'session' or 'self' keys from kwargs to avoid conflicts
            if 'session' in kwargs:
                del kwargs['session']
            if 'self' in kwargs:
                del kwargs['self']

            # Execute the tool function with session as the first parameter after 'self'
            # Since these are bound methods, the call is: method(self, session, **kwargs)
            result = tool(session=session, **kwargs)
            logger.info(f"Tool {name} executed successfully")
            return result
        except Exception as e:
            logger.error(f"Error executing tool {name}: {str(e)}")
            raise
    
    # Placeholder implementations that would connect to the actual MCP server
    # For now, we'll implement direct database operations for demonstration
    def _execute_add_task(self, session=None, **kwargs) -> Dict[str, Any]:
        """Add a new task to the database"""
        if not session:
            raise ValueError("Session is required for database operations")

        from ..models.task import Task
        import uuid
        from datetime import datetime

        # Extract parameters
        title = kwargs.get('title', 'Untitled Task')
        description = kwargs.get('description', '')
        user_id = kwargs.get('user_id')  # This should be passed from the context

        if not user_id:
            raise ValueError("user_id is required to add a task")

        # Ensure user_id is properly converted to UUID if it's a string or integer
        if isinstance(user_id, str):
            try:
                user_id_uuid = uuid.UUID(user_id)
            except ValueError:
                raise ValueError(f"user_id must be a valid UUID string, got: {user_id}")
        elif isinstance(user_id, uuid.UUID):
            user_id_uuid = user_id
        else:
            # If it's neither a string nor UUID, try to convert it
            user_id_uuid = uuid.UUID(str(user_id))

        # Create new task
        new_task = Task(
            id=uuid.uuid4(),
            user_id=user_id_uuid,
            title=title,
            description=description,
            status="incomplete",  # Use canonical 'incomplete' status
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        logger.info(f"Task '{title}' added successfully with ID: {new_task.id}")
        return {
            "status": "created",
            "task_id": str(new_task.id),
            "title": new_task.title,
            "message": f"Task '{title}' added successfully"
        }

    def _execute_list_tasks(self, session=None, **kwargs) -> Dict[str, Any]:
        """List all tasks for the user from the database"""
        if not session:
            raise ValueError("Session is required for database operations")

        from ..models.task import Task
        from sqlmodel import select
        import uuid

        # Extract parameters
        user_id = kwargs.get('user_id')  # This should be passed from the context
        limit = kwargs.get('limit', 50)
        offset = kwargs.get('offset', 0)

        if not user_id:
            raise ValueError("user_id is required to list tasks")

        # Ensure user_id is properly converted to UUID if it's a string
        if isinstance(user_id, str):
            try:
                user_id_uuid = uuid.UUID(user_id)
            except ValueError:
                raise ValueError(f"user_id must be a valid UUID string, got: {user_id}")
        elif isinstance(user_id, uuid.UUID):
            user_id_uuid = user_id
        else:
            # If it's neither a string nor UUID, try to convert it
            user_id_uuid = uuid.UUID(str(user_id))

        # Query tasks for the user
        stmt = select(Task).where(Task.user_id == user_id_uuid).offset(offset).limit(limit)
        tasks = session.exec(stmt).all()

        task_list = []
        for task in tasks:
            task_dict = {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "created_at": task.created_date.isoformat(),  # Using created_at as required
                "updated_at": task.updated_date.isoformat()   # Using updated_at as required
            }
            task_list.append(task_dict)

        logger.info(f"Retrieved {len(tasks)} tasks for user {user_id}")

        # Format tasks according to specification
        formatted_tasks = []
        for task in tasks:
            # Convert status to boolean as per specification
            completed = task.status == "complete"
            task_dict = {
                "id": str(task.id),  # Return as string to match database format
                "title": task.title,
                "completed": completed
            }
            formatted_tasks.append(task_dict)

        message = f"You have {len(tasks)} tasks."
        if tasks:
            # Create a more detailed message if there are tasks
            task_list_str = ", ".join([f"'{task.title}'" for task in tasks])
            message = f"Here are your tasks: {task_list_str}"

        return {
            "status": "success",
            "tasks": formatted_tasks,
            "count": len(formatted_tasks),
            "message": message  # This will be used by the AI agent
        }

    def _resolve_task_identifier(self, session, user_id, task_identifier) -> str:
        """Resolve a task identifier (either UUID or title) to a UUID"""
        from ..models.task import Task
        from sqlmodel import select
        import uuid

        # If the identifier is already a valid UUID string, return it
        try:
            uuid.UUID(task_identifier)
            return task_identifier
        except ValueError:
            # If it's not a UUID, treat it as a task title and search for it
            pass

        # Clean up the task_identifier to extract meaningful text
        # Remove common phrases that might be in the identifier
        cleaned_identifier = task_identifier.lower().strip()

        # Remove common phrases that indicate this is a description rather than an ID
        phrases_to_remove = [
            "task name ",
            "id of ",
            "the ",
            "task",
            "please",
            "can you",
            "i want to",
            "i need to"
        ]

        for phrase in phrases_to_remove:
            cleaned_identifier = cleaned_identifier.replace(phrase, "").strip()

        # If the cleaned identifier is still too short or generic, try to find a real task
        if len(cleaned_identifier) < 2 or cleaned_identifier in ["id", "task", "1", "2", "3", "new", "first", "last", "recent"]:
            # This is likely a placeholder, try to find a real task
            # For "first task" requests, get the most recently created task
            stmt = select(Task).where(
                Task.user_id == uuid.UUID(user_id) if isinstance(user_id, str) else user_id
            ).order_by(Task.created_date.desc()).limit(1)
            matching_tasks = session.exec(stmt).all()

            if matching_tasks:
                return str(matching_tasks[0].id)
            else:
                raise ValueError(f"No tasks found for user {user_id}")
        else:
            # Search for tasks with matching title for this user
            # Try exact match first
            stmt = select(Task).where(
                Task.user_id == uuid.UUID(user_id) if isinstance(user_id, str) else user_id,
                Task.title.ilike(f"{cleaned_identifier}") | Task.title.ilike(f"{cleaned_identifier}%") | Task.title.ilike(f"%{cleaned_identifier}") | Task.title.ilike(f"%{cleaned_identifier}%")
            )
            matching_tasks = session.exec(stmt).all()

            if not matching_tasks:
                raise ValueError(f"No task found with title containing '{cleaned_identifier}'")
            elif len(matching_tasks) > 1:
                # If multiple matches, try to find the best match based on exact title match
                exact_matches = [task for task in matching_tasks if task.title.lower().strip() == cleaned_identifier]
                if exact_matches:
                    return str(exact_matches[0].id)
                else:
                    # If no exact match, return the first match or ask for clarification
                    task_titles = [task.title for task in matching_tasks]
                    raise ValueError(f"Multiple tasks found with title '{cleaned_identifier}': {', '.join(task_titles)}. Please be more specific.")
            else:
                # Exactly one match found
                return str(matching_tasks[0].id)

    def _execute_update_task(self, session=None, **kwargs) -> Dict[str, Any]:
        """Update an existing task in the database"""
        if not session:
            raise ValueError("Session is required for database operations")

        from ..models.task import Task
        from sqlmodel import select
        import uuid
        from datetime import datetime

        # Extract parameters
        task_identifier = kwargs.get('task_id')
        user_id = kwargs.get('user_id')  # This should be passed from the context

        if not task_identifier or not user_id:
            raise ValueError("task_id and user_id are required to update a task")

        # Resolve the task identifier (could be UUID or title)
        task_id = self._resolve_task_identifier(session, user_id, task_identifier)

        # Convert task_id and user_id to UUIDs
        task_id_uuid = uuid.UUID(task_id)
        user_id_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id

        stmt = select(Task).where(
            Task.id == task_id_uuid,
            Task.user_id == user_id_uuid
        )
        task = session.exec(stmt).first()

        if not task:
            raise ValueError(f"Task with ID {task_id} not found for user {user_id}")

        # Update the task with provided parameters, normalizing status values
        updated_fields = []
        if 'title' in kwargs and kwargs['title'] != task.title:
            task.title = kwargs['title']
            updated_fields.append('title')
        if 'description' in kwargs and kwargs['description'] != task.description:
            task.description = kwargs['description']
            updated_fields.append('description')
        if 'status' in kwargs:
            # Normalize status values to canonical form
            status_value = kwargs['status'].lower() if isinstance(kwargs['status'], str) else kwargs['status']
            if status_value in ['complete', 'completed', 'done', 'finished']:
                task.status = 'complete'
            elif status_value in ['incomplete', 'pending', 'todo', 'not_started', 'in progress']:
                task.status = 'incomplete'  # Standardize to 'incomplete' for all non-complete states
            else:
                # If it's not a recognized status, keep as is but log a warning
                logger.warning(f"Unrecognized status value '{status_value}' for task {task_id}, keeping as is")
                task.status = status_value
            updated_fields.append('status')

        task.updated_date = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"Task {task_id} updated successfully")
        return {
            "status": "updated",
            "task_id": str(task.id),
            "title": task.title,
            "message": f"Task '{task.title}' updated successfully"
        }

    def _execute_complete_task(self, session=None, **kwargs) -> Dict[str, Any]:
        """Mark a task as completed in the database"""
        if not session:
            raise ValueError("Session is required for database operations")

        from ..models.task import Task
        from sqlmodel import select
        import uuid
        from datetime import datetime

        # Extract parameters
        task_identifier = kwargs.get('task_id')
        user_id = kwargs.get('user_id')  # This should be passed from the context

        if not task_identifier or not user_id:
            raise ValueError("task_id and user_id are required to complete a task")

        # Resolve the task identifier (could be UUID or title)
        task_id = self._resolve_task_identifier(session, user_id, task_identifier)

        # Convert task_id and user_id to UUIDs
        task_id_uuid = uuid.UUID(task_id)
        user_id_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id

        stmt = select(Task).where(
            Task.id == task_id_uuid,
            Task.user_id == user_id_uuid
        )
        task = session.exec(stmt).first()

        if not task:
            raise ValueError(f"Task with ID {task_id} not found for user {user_id}")

        # Update the task status with canonical value
        task.status = "complete"  # Use canonical 'complete' status
        task.updated_date = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"Task {task_id} marked as completed")
        return {
            "status": "completed",
            "task_id": str(task.id),
            "title": task.title,
            "message": f"Task '{task.title}' marked as completed"
        }

    def _execute_delete_task(self, session=None, **kwargs) -> Dict[str, Any]:
        """Delete a task from the database"""
        if not session:
            raise ValueError("Session is required for database operations")

        from ..models.task import Task
        from sqlmodel import select
        import uuid

        # Extract parameters
        task_identifier = kwargs.get('task_id')
        user_id = kwargs.get('user_id')  # This should be passed from the context

        if not task_identifier or not user_id:
            raise ValueError("task_id and user_id are required to delete a task")

        # Resolve the task identifier (could be UUID or title)
        task_id = self._resolve_task_identifier(session, user_id, task_identifier)

        # Convert task_id and user_id to UUIDs
        task_id_uuid = uuid.UUID(task_id)
        user_id_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id

        stmt = select(Task).where(
            Task.id == task_id_uuid,
            Task.user_id == user_id_uuid
        )
        task = session.exec(stmt).first()

        if not task:
            raise ValueError(f"Task with ID {task_id} not found for user {user_id}")

        # Delete the task
        session.delete(task)
        session.commit()

        logger.info(f"Task {task_id} deleted successfully")
        return {
            "status": "deleted",
            "task_id": str(task.id),
            "title": task.title,
            "message": f"Task '{task.title}' deleted successfully"
        }


# Global instance of the tool registry
tool_registry = ToolRegistry()