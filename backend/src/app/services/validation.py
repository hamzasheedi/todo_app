"""
Validation Service
Provides validation for various inputs and parameters
"""

from typing import Dict, Any, Optional
import uuid


class ValidationService:
    """Service class for validating inputs and parameters"""
    
    @staticmethod
    def validate_uuid(value: str) -> bool:
        """Validate that a string is a valid UUID"""
        try:
            uuid.UUID(value)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_mcp_tool_parameters(tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate parameters for MCP tool execution"""
        errors = []
        
        # Common validation for all tools
        if not isinstance(parameters, dict):
            errors.append("Parameters must be a dictionary")
        
        # Tool-specific validation
        if tool_name == "add_task":
            if "title" not in parameters or not parameters["title"]:
                errors.append("Missing required parameter: title")
            elif len(str(parameters["title"])) > 200:
                errors.append("Title must be 200 characters or less")
                
            if "description" in parameters and parameters["description"]:
                if len(str(parameters["description"])) > 500:
                    errors.append("Description must be 500 characters or less")
        
        elif tool_name == "update_task":
            if "task_id" not in parameters or not parameters["task_id"]:
                errors.append("Missing required parameter: task_id")
            else:
                # According to the specification, task_id can be an integer, UUID string, or task title
                task_id = parameters["task_id"]
                if isinstance(task_id, int):
                    # If it's an integer, convert to string
                    task_id_str = str(task_id)
                    parameters["task_id"] = task_id_str
                elif isinstance(task_id, str):
                    # Keep as string - it could be a UUID or a task title
                    task_id_str = task_id
                    # Don't validate as UUID here since it might be a task title
                    # The tool will handle resolution of task titles to UUIDs
                else:
                    errors.append(f"task_id must be a string or integer, got: {type(task_id).__name__}")

            # Validate optional status parameter and normalize values
            if "status" in parameters and parameters["status"]:
                status_value = str(parameters["status"]).lower()
                if status_value in ["complete", "completed", "done", "finished"]:
                    parameters["status"] = "complete"
                elif status_value in ["incomplete", "pending", "todo", "not started", "in progress"]:
                    parameters["status"] = "incomplete"
                elif status_value not in ["complete", "incomplete"]:
                    errors.append(f"status must be a valid value, got: {status_value}")

        elif tool_name == "complete_task":
            if "task_id" not in parameters or not parameters["task_id"]:
                errors.append("Missing required parameter: task_id")
            else:
                # According to the specification, task_id can be an integer, UUID string, or task title
                task_id = parameters["task_id"]
                if isinstance(task_id, int):
                    # If it's an integer, convert to string
                    task_id_str = str(task_id)
                    parameters["task_id"] = task_id_str
                elif isinstance(task_id, str):
                    # Keep as string - it could be a UUID or a task title
                    task_id_str = task_id
                    # Don't validate as UUID here since it might be a task title
                    # The tool will handle resolution of task titles to UUIDs
                else:
                    errors.append(f"task_id must be a string or integer, got: {type(task_id).__name__}")

        elif tool_name == "delete_task":
            if "task_id" not in parameters or not parameters["task_id"]:
                errors.append("Missing required parameter: task_id")
            else:
                # According to the specification, task_id can be an integer, UUID string, or task title
                task_id = parameters["task_id"]
                if isinstance(task_id, int):
                    # If it's an integer, convert to string
                    task_id_str = str(task_id)
                    parameters["task_id"] = task_id_str
                elif isinstance(task_id, str):
                    # Keep as string - it could be a UUID or a task title
                    task_id_str = task_id
                    # Don't validate as UUID here since it might be a task title
                    # The tool will handle resolution of task titles to UUIDs
                else:
                    errors.append(f"task_id must be a string or integer, got: {type(task_id).__name__}")
        
        elif tool_name == "list_tasks":
            # Validate optional parameters
            if "limit" in parameters and parameters["limit"] is not None:
                try:
                    # Convert to int to handle both string and numeric values
                    limit = int(parameters["limit"])
                    if limit <= 0 or limit > 100:
                        errors.append("limit must be between 1 and 100")
                    else:
                        # Normalize the limit value
                        parameters["limit"] = limit
                except (ValueError, TypeError):
                    errors.append("limit must be a valid integer")
            else:
                # Set default limit if not provided
                parameters["limit"] = 50

            if "offset" in parameters and parameters["offset"] is not None:
                try:
                    # Convert to int to handle both string and numeric values
                    offset = int(parameters["offset"])
                    if offset < 0:
                        errors.append("offset must be a non-negative integer")
                    else:
                        # Normalize the offset value
                        parameters["offset"] = offset
                except (ValueError, TypeError):
                    errors.append("offset must be a valid integer")
            else:
                # Set default offset if not provided
                parameters["offset"] = 0
        
        if errors:
            raise ValueError(f"Validation errors: {'; '.join(errors)}")

        # Convert task_id to string for task-related tools if needed
        if tool_name in ["update_task", "complete_task", "delete_task"] and "task_id" in parameters:
            parameters["task_id"] = str(parameters["task_id"])

        # Convert user_id to string if it's provided
        if "user_id" in parameters and parameters["user_id"]:
            # If user_id is provided, ensure it's a valid UUID string
            user_id_val = parameters["user_id"]
            if isinstance(user_id_val, (int, float)):
                # If it's a number, try to convert to string UUID format
                parameters["user_id"] = str(user_id_val)
            elif isinstance(user_id_val, str):
                # If it's already a string, keep as is
                parameters["user_id"] = user_id_val
            else:
                # If it's another type, convert to string
                parameters["user_id"] = str(user_id_val)

        return parameters
    
    @staticmethod
    def validate_ai_request(user_input: str) -> Dict[str, Any]:
        """Validate an incoming AI request"""
        errors = []
        
        if not user_input or not user_input.strip():
            errors.append("User input cannot be empty")
        
        if len(user_input) > 500:
            errors.append("User input must be 500 characters or less")
        
        if errors:
            raise ValueError(f"Validation errors: {'; '.join(errors)}")
        
        return {"input_valid": True}