"""
MCP Server
Implements the Model Context Protocol server for task operations
"""

import asyncio
from typing import Dict, Any, Optional
from .monitoring import MonitoringService
from sqlmodel import Session


class MCPServer:
    """
    Model Context Protocol server implementation for task operations.
    This is a simplified implementation that connects to the actual MCP server.
    """
    
    def __init__(self, session: Session):
        self.session = session
        self.tools = {
            "add_task": self._handle_add_task,
            "list_tasks": self._handle_list_tasks,
            "update_task": self._handle_update_task,
            "complete_task": self._handle_complete_task,
            "delete_task": self._handle_delete_task
        }
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any], user_id: str, 
                          conversation_id: str) -> Dict[str, Any]:
        """
        Execute an MCP tool with the given parameters
        """
        if tool_name not in self.tools:
            error_msg = f"Tool '{tool_name}' is not supported"
            MonitoringService.log_tool_invocation(
                self.session, tool_name, user_id, conversation_id, 
                parameters, success=False, error_msg=error_msg
            )
            return {"error": error_msg}
        
        try:
            # Log the tool invocation
            MonitoringService.log_tool_invocation(
                self.session, tool_name, user_id, conversation_id, 
                parameters, success=True
            )
            
            # Execute the tool
            result = await self.tools[tool_name](parameters, user_id)
            
            return {
                "success": True,
                "result": result,
                "tool_name": tool_name
            }
        except Exception as e:
            error_msg = str(e)
            MonitoringService.log_tool_invocation(
                self.session, tool_name, user_id, conversation_id, 
                parameters, success=False, error_msg=error_msg
            )
            
            return {
                "success": False,
                "error": error_msg,
                "tool_name": tool_name
            }
    
    async def _handle_add_task(self, parameters: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Handle the add_task tool
        """
        # In a real implementation, this would call the actual task service
        # to add a task to the database
        title = parameters.get("title", "")
        description = parameters.get("description", "")
        
        # Validate parameters
        if not title:
            raise ValueError("Title is required for add_task")
        
        # Simulate calling the actual task service
        # In a real implementation, this would be an actual call to create a task
        task_data = {
            "id": "mock-task-id",  # This would be a real UUID in production
            "title": title,
            "description": description,
            "status": "incomplete",
            "user_id": user_id
        }
        
        return {"message": f"Task '{title}' added successfully", "task": task_data}
    
    async def _handle_list_tasks(self, parameters: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Handle the list_tasks tool
        """
        # In a real implementation, this would call the actual task service
        # to retrieve tasks from the database
        
        # Extract optional parameters
        limit = parameters.get("limit", 50)
        offset = parameters.get("offset", 0)
        
        # Simulate calling the actual task service
        # In a real implementation, this would return actual tasks from the database
        tasks = [
            {
                "id": "mock-task-1",
                "title": "Sample Task 1",
                "description": "This is a sample task",
                "status": "incomplete",
                "user_id": user_id
            },
            {
                "id": "mock-task-2", 
                "title": "Sample Task 2",
                "description": "This is another sample task",
                "status": "complete",
                "user_id": user_id
            }
        ]
        
        return {
            "tasks": tasks[offset:offset+limit],
            "total_count": len(tasks),
            "returned_count": min(limit, len(tasks)-offset)
        }
    
    async def _handle_update_task(self, parameters: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Handle the update_task tool
        """
        task_id = parameters.get("task_id")
        if not task_id:
            raise ValueError("task_id is required for update_task")
        
        # Extract optional parameters
        title = parameters.get("title")
        description = parameters.get("description")
        status = parameters.get("status")
        
        # Simulate calling the actual task service
        # In a real implementation, this would update the task in the database
        updated_fields = {}
        if title:
            updated_fields["title"] = title
        if description:
            updated_fields["description"] = description
        if status:
            updated_fields["status"] = status
        
        return {
            "message": f"Task {task_id} updated successfully",
            "updated_fields": updated_fields
        }
    
    async def _handle_complete_task(self, parameters: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Handle the complete_task tool
        """
        task_id = parameters.get("task_id")
        if not task_id:
            raise ValueError("task_id is required for complete_task")
        
        # Simulate calling the actual task service
        # In a real implementation, this would update the task status in the database
        return {
            "message": f"Task {task_id} marked as complete",
            "task_id": task_id
        }
    
    async def _handle_delete_task(self, parameters: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Handle the delete_task tool
        """
        task_id = parameters.get("task_id")
        if not task_id:
            raise ValueError("task_id is required for delete_task")
        
        # Simulate calling the actual task service
        # In a real implementation, this would delete the task from the database
        return {
            "message": f"Task {task_id} deleted successfully",
            "task_id": task_id
        }


# Async wrapper for synchronous calls
def run_mcp_tool_sync(mcp_server: MCPServer, tool_name: str, parameters: Dict[str, Any], 
                     user_id: str, conversation_id: str) -> Dict[str, Any]:
    """
    Synchronous wrapper for running MCP tools
    """
    async def run_async():
        return await mcp_server.execute_tool(tool_name, parameters, user_id, conversation_id)
    
    # Note: In a real implementation, you'd want to properly handle the async nature
    # This is a simplified approach for demonstration
    import concurrent.futures
    import threading
    
    def run_in_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(run_async())
        finally:
            loop.close()
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(run_in_thread)
        return future.result()