"""
AI Agent Service
Handles AI processing and tool orchestration
"""

from openai import OpenAI
from typing import Dict, Any, Optional, List
import json
import logging
from .ai_provider_factory import AIProviderFactory
from .fallback_handler import FallbackHandler, CircuitBreaker
from .timeout_handler import TimeoutManager
from .tool_registry import tool_registry
from .validation import ValidationService
from ..config.ai_settings import AISettings


logger = logging.getLogger(__name__)


class AIAgentService:
    """Service class for handling AI processing and tool orchestration"""
    
    def __init__(self):
        self.primary_client = AIProviderFactory.create_primary_client()
        self.fallback_client = AIProviderFactory.create_fallback_client()
        self.tools = tool_registry.list_available_tools()

    def _classify_user_intent(self, user_message: str) -> str:
        """Classify the user's intent to determine which tool to use"""
        message_lower = user_message.lower().strip()

        # Define keywords for each intent with higher precision
        list_keywords = [
            "show my", "list my", "my tasks", "what tasks", "view tasks", "see tasks",
            "display tasks", "list tasks", "show tasks", "my to-do", "what do i have",
            "current tasks", "active tasks", "open tasks", "tasks list", "task list",
            "what am i working on", "my todo", "list all", "show all", "what's on my list"
        ]

        add_keywords = [
            "add task", "create task", "new task", "make task", "add a task",
            "create a task", "make a task", "add to my", "add to list", "put on my list",
            "i need to", "i want to", "create a new", "add something", "make a new"
        ]

        update_keywords = [
            "update task", "change task", "modify task", "edit task", "update my",
            "change my", "modify my", "edit my", "update the", "change the"
        ]

        complete_keywords = [
            "complete task", "finish task", "mark as complete", "mark as done",
            "complete", "finish", "done", "tick off", "check off", "mark done",
            "mark complete", "finish up", "complete the", "finish the"
        ]

        delete_keywords = [
            "delete task", "remove task", "erase task", "delete from",
            "remove from", "get rid of task", "kill task", "remove the",
            "delete the", "erase the", "get rid of", "remove this", "delete this"
        ]

        # Enhanced intent classification with conflict detection
        intents_found = []

        # Check for list intent
        if any(keyword in message_lower for keyword in list_keywords):
            intents_found.append("list_tasks")

        # Check for add intent
        if any(keyword in message_lower for keyword in add_keywords):
            intents_found.append("add_task")

        # Check for update intent
        if any(keyword in message_lower for keyword in update_keywords):
            intents_found.append("update_task")

        # Check for complete intent
        if any(keyword in message_lower for keyword in complete_keywords):
            intents_found.append("complete_task")

        # Check for delete intent
        if any(keyword in message_lower for keyword in delete_keywords):
            intents_found.append("delete_task")

        # If multiple intents found, prioritize based on context
        if len(intents_found) > 1:
            # If list is among intents and message is asking about existing tasks, prioritize list
            if "list_tasks" in intents_found and any(phrase in message_lower for phrase in ["my", "current", "existing", "show", "list"]):
                return "list_tasks"

        # If exactly one intent found, return it
        if len(intents_found) == 1:
            return intents_found[0]

        # If no specific intent found, check for general task inquiries
        if "task" in message_lower and any(q_word in message_lower for q_word in ["what", "where", "how", "do i", "my", "list", "show", "see"]):
            return "list_tasks"

        # Default intent if none clearly matches
        return "unknown"
    
    def process_user_message(self, user_message: str, conversation_context: Optional[List[Dict[str, str]]] = None, user_tasks: Optional[List] = None, session=None, user_id=None) -> Dict[str, Any]:
        """
        Process a user message and return an appropriate response
        """
        # Classify user intent before processing
        intent = self._classify_user_intent(user_message)
        logger.info(f"Detected user intent: {intent}")

        # Validate the user input
        ValidationService.validate_ai_request(user_message)

        # Prepare the conversation context
        messages = []

        # Add system message to provide context about available tools and when to use them
        system_message = {
            "role": "system",
            "content": (
                "You are an AI assistant that helps users manage their tasks. "
                "You have access to specific tools for task management operations. "
                "Follow these rules:\n"
                "1. Use 'list_tasks' when users ask to see, show, list, view, display, or get their tasks.\n"
                "2. Use 'add_task' only when users explicitly request to add, create, or make a new task.\n"
                "3. Use 'update_task' when users want to modify, edit, change, or rename an existing task.\n"
                "4. Use 'complete_task' when users want to finish, complete, mark as done, or check off a task.\n"
                "5. Use 'delete_task' when users want to remove, delete, erase, or eliminate a task.\n"
                "6. Always use the appropriate tool based on user intent rather than creating tasks unnecessarily.\n"
                "7. If a user wants to see their tasks, use list_tasks first, then respond based on the results.\n"
                "8. Never create a task when the user only wants to view their existing tasks."
            )
        }
        messages.append(system_message)

        if conversation_context:
            messages.extend(conversation_context)

        # Add the user's message
        # If user_tasks is provided and the message is a task query, add task context
        message_content = user_message

        # Prevent unintended task creation when user intent is to list/view tasks
        if intent == "list_tasks" and user_tasks is not None:
            if user_tasks:
                task_context = "Here are your current tasks:\n"
                for task in user_tasks:
                    status_text = "✓ Completed" if task.status == "complete" else "○ Pending"
                    task_context += f"- [{status_text}] {task.title} (Created: {task.created_date.strftime('%m/%d/%Y')})\n"
                message_content = f"{user_message}\n\n{task_context}"
            else:
                message_content = f"{user_message}\n\nYou don't have any tasks yet."

        messages.append({"role": "user", "content": message_content})

        # Define available tools for the AI
        tools_schema = self._get_tools_schema()

        try:
            # Attempt to get a response from the AI with tools
            response = self._call_ai_with_tools(messages, tools_schema, session=session, user_id=user_id)

            # Process the response
            result = self._process_ai_response(response, session=session, user_id=user_id)
            return result

        except Exception as e:
            logger.error(f"Error processing user message: {str(e)}")

            # Try with fallback if available
            if self.fallback_client:
                logger.info("Attempting fallback client...")
                try:
                    response = self._call_ai_with_tools(messages, tools_schema, session=session, user_id=user_id, use_fallback=True)
                    result = self._process_ai_response(response, session=session, user_id=user_id)
                    return result
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed: {str(fallback_error)}")

            # If everything fails, return an error response
            return {
                "response": "I'm sorry, but I'm currently experiencing difficulties. Please try again later.",
                "tool_calls": [],
                "error": str(e)
            }
    
    def _call_ai_with_tools(self, messages: List[Dict[str, str]], tools_schema: List[Dict[str, Any]], session=None, user_id=None, use_fallback: bool = False) -> Any:
        """Call the AI with tools - with proper tool calling cycle implementation"""
        client = self.fallback_client if use_fallback else self.primary_client

        if not client:
            raise Exception("No AI client available")

        # Execute with timeout
        def call_ai():
            # Make a copy of messages to avoid modifying the original
            current_messages = messages.copy()

            try:
                # Start with the initial request
                response = client.chat.completions.create(
                    model=AISettings.AI_MODEL,
                    messages=current_messages,
                    tools=tools_schema,
                    tool_choice="auto",
                    temperature=0.7,
                    max_tokens=1000
                )

                # Handle the complete tool calling cycle
                # If the response contains tool calls, we need to execute them and send results back
                # Limit iterations to prevent infinite loops
                max_iterations = 5
                iteration = 0

                # Check if the response has tool calls that need to be executed
                while (hasattr(response.choices[0], 'finish_reason') and
                       response.choices[0].finish_reason == "tool_calls" and
                       hasattr(response.choices[0].message, 'tool_calls') and
                       response.choices[0].message.tool_calls and
                       iteration < max_iterations):
                    iteration += 1

                    # Add the assistant's message with tool calls to the conversation
                    current_messages.append(response.choices[0].message)

                    # Process each tool call
                    for tool_call in response.choices[0].message.tool_calls:
                        # Execute the tool and get the result
                        try:
                            function_name = tool_call.function.name
                            function_args = json.loads(tool_call.function.arguments)

                            # Add user_id to arguments if it's a task-related tool
                            if function_name in ["add_task", "list_tasks", "update_task", "complete_task", "delete_task"]:
                                function_args["user_id"] = str(user_id) if user_id else None

                            # Validate the arguments
                            validated_args = ValidationService.validate_mcp_tool_parameters(function_name, function_args)

                            # Execute the tool with session and user context
                            tool_result = tool_registry.execute_tool(function_name, session=session, **validated_args)

                            # Add the tool result to the messages
                            current_messages.append({
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": json.dumps(tool_result)
                            })
                        except Exception as e:
                            logger.error(f"Error executing tool {tool_call.function.name}: {str(e)}")
                            # Add error message as tool result
                            current_messages.append({
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": json.dumps({"error": str(e)})
                            })

                    # Make another request with the tool results
                    response = client.chat.completions.create(
                        model=AISettings.AI_MODEL,
                        messages=current_messages,
                        tools=tools_schema,
                        tool_choice="auto",
                        temperature=0.7,
                        max_tokens=1000
                    )

                return response
            except Exception as e:
                # If tool calling fails completely (e.g., schema validation at API level),
                # fall back to a simple completion without tools
                logger.warning(f"Tool calling failed, falling back to simple completion: {e}")

                # Return a simple completion without tools
                return client.chat.completions.create(
                    model=AISettings.AI_MODEL,
                    messages=messages,  # Use original messages
                    temperature=0.7,
                    max_tokens=1000
                )

        timeout = AISettings.AI_TIMEOUT
        return TimeoutManager.execute_with_timeout(call_ai, timeout)

    def _is_valid_uuid(self, val: str) -> bool:
        """Check if a string is a valid UUID"""
        import uuid
        try:
            uuid.UUID(val)
            return True
        except ValueError:
            return False
    
    def _get_tools_schema(self) -> List[Dict[str, Any]]:
        """Get the schema for available tools"""
        tools_schema = []

        for tool_name in self.tools:
            description = tool_registry.get_tool_description(tool_name)

            # Create a basic schema for each tool
            tool_schema = {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": description,
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }

            # Add specific parameters for known tools
            if tool_name == "add_task":
                tool_schema["function"]["parameters"]["properties"] = {
                    "title": {"type": "string", "description": "The title of the task"},
                    "description": {"type": "string", "description": "The description of the task"}
                }
                tool_schema["function"]["parameters"]["required"] = ["title"]

                # Enhanced description with clear usage instructions for the AI
                tool_schema["function"]["description"] = (
                    "Add a new task to the user's task list. "
                    "Use this ONLY when the user explicitly requests to add, create, or make a new task. "
                    "Examples: 'Add a task to buy groceries', 'Create a task to call mom', 'I need to remember to pay bills'. "
                    "NEVER use this when the user wants to list, view, update, complete, or delete tasks. "
                    "The title parameter is required. Description is optional."
                )

            elif tool_name == "update_task":
                tool_schema["function"]["parameters"]["properties"] = {
                    "task_id": {
                        "anyOf": [{"type": "string"}, {"type": "integer"}],  # Accept both string UUIDs and integer IDs
                        "description": "The ID of the task to update (can be the task's UUID string or its integer position in the list)"
                    },
                    "title": {"type": "string", "description": "The new title of the task"},
                    "description": {"type": "string", "description": "The new description of the task"},
                    "status": {"type": "string", "description": "The new status of the task ('incomplete' or 'complete')"}
                }
                tool_schema["function"]["parameters"]["required"] = ["task_id"]

                # Enhanced description with clear usage instructions for the AI
                tool_schema["function"]["description"] = (
                    "Update an existing task in the user's task list. "
                    "Use this when the user requests to modify, edit, change, rename, or update an existing task by specifying its ID and the fields to update. "
                    "Examples: 'Change the title of task 1', 'Update task 2 to have a new description', 'Update the task called \"buy groceries\"', 'Edit task with ID abc-123'. "
                    "NEVER use this when the user wants to add, list, complete, or delete tasks. "
                    "The task_id parameter is required and can be either a UUID string or an integer ID. "
                    "At least one of title, description, or status must be provided to update."
                )

            elif tool_name == "complete_task":
                tool_schema["function"]["parameters"]["properties"] = {
                    "task_id": {
                        "anyOf": [{"type": "string"}, {"type": "integer"}],  # Accept both string UUIDs and integer IDs
                        "description": "The ID of the task to complete (can be the task's UUID string or its integer position in the list)"
                    }
                }
                tool_schema["function"]["parameters"]["required"] = ["task_id"]

                # Enhanced description with clear usage instructions for the AI
                tool_schema["function"]["description"] = (
                    "Mark a task as completed. "
                    "Use this when the user requests to finish, complete, mark as done, mark as finished, check off, or tick off a specific task by its ID. "
                    "Examples: 'Complete task 1', 'Mark task 2 as done', 'Finish the task called \"buy groceries\"', 'Check off task with ID abc-123', 'Complete the first task'. "
                    "NEVER use this when the user wants to add, list, update, or delete tasks. "
                    "The task_id parameter is required and can be either a UUID string or an integer ID representing the task to complete."
                )

            elif tool_name == "delete_task":
                tool_schema["function"]["parameters"]["properties"] = {
                    "task_id": {
                        "anyOf": [{"type": "string"}, {"type": "integer"}],  # Accept both string UUIDs and integer IDs
                        "description": "The ID of the task to delete (can be the task's UUID string or its integer position in the list)"
                    }
                }
                tool_schema["function"]["parameters"]["required"] = ["task_id"]

                # Enhanced description with clear usage instructions for the AI
                tool_schema["function"]["description"] = (
                    "Delete a task from the user's task list. "
                    "Use this when the user requests to remove, delete, erase, eliminate, kill, or get rid of a specific task by its ID. "
                    "Examples: 'Delete task 1', 'Remove task 2', 'Erase the task called \"buy groceries\"', 'Kill task with ID abc-123', 'Delete the first task'. "
                    "NEVER use this when the user wants to add, list, update, or complete tasks. "
                    "The task_id parameter is required and can be either a UUID string or an integer ID representing the task to delete."
                )

            elif tool_name == "list_tasks":
                tool_schema["function"]["parameters"]["properties"] = {
                    "limit": {"type": "integer", "description": "Maximum number of tasks to return (default 50)", "default": 50},
                    "offset": {"type": "integer", "description": "Offset for pagination (default 0)", "default": 0}
                }
                # These are optional parameters, so we don't add them to required

                # Enhanced description with clear usage instructions for the AI
                tool_schema["function"]["description"] = (
                    "Retrieve all tasks for the user. "
                    "Use this when the user asks to see, list, view, show, display, get, or retrieve their tasks, to-do items, or anything related to viewing existing tasks. "
                    "Examples: 'Show me my tasks', 'List all my tasks', 'What tasks do I have?', 'Display my to-do list', 'View my tasks'. "
                    "NEVER use this when the user wants to add, create, update, complete, or delete tasks. "
                    "The response will include an array of tasks with id, title, and completed status. "
                    "Use limit and offset for pagination if the user has many tasks."
                )

            tools_schema.append(tool_schema)

        return tools_schema
    
    def _process_ai_response(self, response: Any, session=None, user_id=None) -> Dict[str, Any]:
        """Process the AI response and execute any required tools with proper intent classification and safety checks"""
        choice = response.choices[0]
        message = choice.message

        result = {
            "response": message.content or "",
            "tool_calls": []
        }

        # Process any tool calls in the response
        if message.tool_calls:
            # Process each tool call in sequence
            for tool_call in message.tool_calls:
                try:
                    # Extract tool name and arguments
                    tool_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)

                    # Validate that session is available for database operations
                    if not session and tool_name in ["add_task", "list_tasks", "update_task", "complete_task", "delete_task"]:
                        raise ValueError(f"Session is required for {tool_name} operation")

                    # Add user_id to arguments if it's a task-related tool
                    if tool_name in ["add_task", "list_tasks", "update_task", "complete_task", "delete_task"]:
                        arguments["user_id"] = str(user_id) if user_id else None

                    # Special handling for task operations that might have task names instead of IDs
                    if tool_name in ["update_task", "complete_task", "delete_task"] and "task_id" in arguments:
                        # If task_id looks like a task name rather than a UUID, try to resolve it
                        task_id_value = arguments["task_id"]
                        if isinstance(task_id_value, str) and not self._is_valid_uuid(task_id_value):
                            # This might be a task name or description, try to resolve it to a real task ID
                            try:
                                resolved_task_id = tool_registry._resolve_task_identifier(session, user_id, task_id_value)
                                arguments["task_id"] = resolved_task_id
                                logger.info(f"Resolved task identifier '{task_id_value}' to UUID '{resolved_task_id}'")
                            except ValueError as e:
                                logger.warning(f"Could not resolve task identifier '{task_id_value}': {str(e)}")
                                # Keep the original value and let validation handle it

                    # Validate the arguments against the tool schema
                    validated_args = ValidationService.validate_mcp_tool_parameters(tool_name, arguments)

                    # Execute the tool with session and user context
                    tool_result = tool_registry.execute_tool(tool_name, session=session, **validated_args)

                    # Add to results
                    result["tool_calls"].append({
                        "tool_name": tool_name,
                        "parameters": validated_args,
                        "result": tool_result
                    })

                    # Update the response if needed based on tool results
                    # According to the specification, tools return structured responses
                    if tool_result.get("message"):
                        result["response"] = tool_result["message"]
                    elif tool_name == "list_tasks" and "tasks" in tool_result:
                        # Format the task list response according to specification
                        tasks = tool_result["tasks"]
                        if tasks:
                            task_list = []
                            for task in tasks:
                                status_text = "✓" if task.get("completed", False) else "○"
                                task_list.append(f"- [{status_text}] {task.get('title', 'Untitled Task')}")
                            result["response"] = f"Here are your tasks:\n" + "\n".join(task_list)
                        else:
                            result["response"] = "You don't have any tasks yet."

                except Exception as e:
                    logger.error(f"Error executing tool {tool_call.function.name}: {str(e)}")
                    result["tool_calls"].append({
                        "tool_name": tool_call.function.name,
                        "parameters": json.loads(tool_call.function.arguments),
                        "error": str(e)
                    })
        else:
            # If there are no tool calls, just return the content
            result["response"] = message.content or ""

        # Ensure there's always a meaningful response for the user
        if not result["response"] and result["tool_calls"]:
            # If there are tool calls but no response content, create a meaningful response
            successful_tool_calls = [tc for tc in result["tool_calls"] if "error" not in tc]
            if successful_tool_calls:
                # Check if any of the successful calls was a list_tasks call
                list_task_results = [tc for tc in successful_tool_calls if tc["tool_name"] == "list_tasks"]
                if list_task_results:
                    # Use the message from the list_tasks result which contains formatted tasks
                    list_result = list_task_results[0]["result"]
                    if "message" in list_result:
                        result["response"] = list_result["message"]
                    else:
                        # Fallback if no message in result
                        result["response"] = f"You have {list_result.get('count', 0)} tasks."
                else:
                    # For other tool calls, use general message
                    tool_names = [tc["tool_name"] for tc in successful_tool_calls]
                    result["response"] = f"Action(s) completed: {', '.join(set(tool_names))}."
            else:
                result["response"] = "I attempted to process your request but encountered some issues with the required actions."
        elif not result["response"]:
            # If there's no response and no tool calls, provide a default
            result["response"] = "I processed your request but don't have specific information to share."

        return result