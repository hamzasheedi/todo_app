"""
MCP Tool Invocation Model
Represents a call to an MCP tool, including parameters and authentication context
"""

from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime
from sqlalchemy import JSON, Column


class MCPToolInvocation(SQLModel, table=True, extend_existing=True):
    """
    Represents a call to an MCP tool, including parameters and authentication context
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tool_name: str = Field(description="Name of the MCP tool being invoked (e.g., 'add_task', 'list_tasks')")
    parameters: str = Field(default=None, sa_column=Column(JSON), description="Parameters passed to the tool")
    conversation_id: uuid.UUID = Field(description="Foreign key to the conversation that triggered this invocation")
    user_id: uuid.UUID = Field(description="Foreign key to the user who initiated the request")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the tool was invoked")
    status: str = Field(default="pending", description="Status of the invocation ('pending', 'success', 'failed')")
    result: Optional[str] = Field(default=None, sa_column=Column(JSON), description="Result returned by the tool")
    error_message: Optional[str] = Field(default=None, description="Error message if the invocation failed")