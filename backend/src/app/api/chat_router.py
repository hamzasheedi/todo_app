"""
Chat Router
Handles chat endpoint requests and orchestrates the AI processing
"""

import json
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid
from sqlmodel import Session

from ..database.database import get_session
from ..auth.backend_jwt import get_current_user_from_backend_jwt
from ..models.user import User
from ..services.conversation_service import ConversationService
from ..services.ai_agent_service import AIAgentService
from ..services.validation import ValidationService


router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500, description="The user's message to the chatbot")
    conversation_id: Optional[str] = Field(None, description="Optional ID of existing conversation to continue")


class ChatResponse(BaseModel):
    response: str = Field(..., description="The chatbot's response to the user")
    conversation_id: str = Field(..., description="The ID of the conversation")
    tool_calls: Optional[List[Dict[str, Any]]] = Field(default=[], description="List of tools that were called")


class ToolCallResponse(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None


@router.post("/", response_model=ChatResponse)
async def process_chat_message(
    request: ChatRequest,
    current_user: User = Depends(get_current_user_from_backend_jwt),
    session: Session = Depends(get_session)
):
    """
    Process a user message and return an AI-generated response.
    The AI processes the message and may invoke MCP tools to perform task operations.
    Conversation state is maintained in the database.
    """
    try:
        # Validate the request
        ValidationService.validate_ai_request(request.message)

        # Special handling for task-related queries
        message_lower = request.message.lower()
        if any(keyword in message_lower for keyword in ["show my tasks", "list my tasks", "my tasks", "what tasks do i have", "show me my tasks"]):
            # Fetch user's tasks directly from the database
            from ..models.task import Task
            from sqlmodel import select

            # Query tasks for the current user
            user_tasks = session.exec(
                select(Task).where(Task.user_id == current_user.id)
            ).all()

            # Initialize the AI agent service
            ai_agent = AIAgentService()

            # Get or create conversation
            conversation = None
            if request.conversation_id:
                if not ValidationService.validate_uuid(request.conversation_id):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid conversation ID format"
                    )

                conversation = ConversationService.get_conversation(
                    session,
                    uuid.UUID(request.conversation_id),
                    current_user.id
                )

                if not conversation:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Conversation not found"
                    )
            else:
                conversation = ConversationService.create_conversation(
                    session,
                    current_user.id,
                    title=request.message[:50] + "..." if len(request.message) > 50 else request.message
                )

            # Get conversation context for the AI
            messages = json.loads(conversation.messages) if conversation.messages else []
            conversation_context = [
                {"role": msg.get("role", "user"), "content": msg.get("content", "")}
                for msg in messages[-10:]  # Use last 10 messages as context
            ]

            # Process the user message with AI, passing the user's tasks
            ai_response = ai_agent.process_user_message(request.message, conversation_context, user_tasks=user_tasks, session=session, user_id=current_user.id)

            # Add user message to conversation
            ConversationService.add_message_to_conversation(
                session,
                conversation.id,
                "user",
                request.message
            )

            # Add AI response to conversation
            ConversationService.add_message_to_conversation(
                session,
                conversation.id,
                "assistant",
                ai_response.get("response", "")
            )

            # Update conversation timestamp
            ConversationService.update_conversation(session, conversation)

            # Prepare the response
            response_text = ai_response.get("response", "").strip()
            if not response_text:
                # If the AI didn't provide a meaningful response, create one based on tool calls
                tool_calls = ai_response.get("tool_calls", [])
                if tool_calls:
                    successful_calls = [tc for tc in tool_calls if "error" not in tc]
                    if successful_calls:
                        response_text = "Your request has been processed successfully."
                    else:
                        response_text = "I attempted to process your request but encountered some issues."
                else:
                    response_text = "I processed your request."

            response_data = ChatResponse(
                response=response_text,
                conversation_id=str(conversation.id),
                tool_calls=ai_response.get("tool_calls", [])
            )

            return response_data

        # For non-task queries, use the AI agent
        # Initialize the AI agent service
        ai_agent = AIAgentService()

        # Get or create conversation
        conversation = None
        if request.conversation_id:
            # Validate conversation ID format
            if not ValidationService.validate_uuid(request.conversation_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid conversation ID format"
                )

            conversation = ConversationService.get_conversation(
                session,
                uuid.UUID(request.conversation_id),
                current_user.id
            )

            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found"
                )
        else:
            # Create a new conversation
            conversation = ConversationService.create_conversation(
                session,
                current_user.id,
                title=request.message[:50] + "..." if len(request.message) > 50 else request.message
            )

        # Get conversation context for the AI
        messages = json.loads(conversation.messages) if conversation.messages else []
        conversation_context = [
            {"role": msg.get("role", "user"), "content": msg.get("content", "")}
            for msg in messages[-10:]  # Use last 10 messages as context
        ]

        # Process the user message with AI
        ai_response = ai_agent.process_user_message(request.message, conversation_context, session=session, user_id=current_user.id)

        # Add user message to conversation
        ConversationService.add_message_to_conversation(
            session,
            conversation.id,
            "user",
            request.message
        )

        # Add AI response to conversation
        ConversationService.add_message_to_conversation(
            session,
            conversation.id,
            "assistant",
            ai_response.get("response", "")
        )

        # Update conversation timestamp
        ConversationService.update_conversation(session, conversation)

        # Prepare the response
        response_text = ai_response.get("response", "").strip()
        if not response_text:
            # If the AI didn't provide a meaningful response, create one based on tool calls
            tool_calls = ai_response.get("tool_calls", [])
            if tool_calls:
                successful_calls = [tc for tc in tool_calls if "error" not in tc]
                if successful_calls:
                    response_text = "Your request has been processed successfully."
                else:
                    response_text = "I attempted to process your request but encountered some issues."
            else:
                response_text = "I processed your request."

        response_data = ChatResponse(
            response=response_text,
            conversation_id=str(conversation.id),
            tool_calls=ai_response.get("tool_calls", [])
        )

        return response_data

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error
        import logging
        logging.error(f"Error processing chat message: {str(e)}")

        # Return a user-friendly error response
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request"
        )


# Additional endpoints for conversation management

class ConversationSummary(BaseModel):
    id: str
    title: Optional[str]
    created_at: str
    updated_at: str


class ListConversationsResponse(BaseModel):
    conversations: List[ConversationSummary]


@router.get("/conversations/", response_model=ListConversationsResponse)
async def list_user_conversations(
    current_user: User = Depends(get_current_user_from_backend_jwt),
    session: Session = Depends(get_session)
):
    """
    List all conversations for the authenticated user
    """
    try:
        conversations = ConversationService.get_user_conversations(session, current_user.id)
        
        summaries = []
        for conv in conversations:
            summaries.append(
                ConversationSummary(
                    id=str(conv.id),
                    title=conv.title,
                    created_at=conv.created_at.isoformat(),
                    updated_at=conv.updated_at.isoformat()
                )
            )
        
        return ListConversationsResponse(conversations=summaries)
        
    except Exception as e:
        import logging
        logging.error(f"Error listing conversations: {str(e)}")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving conversations"
        )


class ConversationDetail(BaseModel):
    id: str
    title: Optional[str]
    created_at: str
    updated_at: str
    messages: List[Dict[str, Any]]


@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
async def get_conversation_detail(
    conversation_id: str,
    current_user: User = Depends(get_current_user_from_backend_jwt),
    session: Session = Depends(get_session)
):
    """
    Get the full history of a specific conversation
    """
    try:
        # Validate conversation ID format
        if not ValidationService.validate_uuid(conversation_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid conversation ID format"
            )
        
        conversation = ConversationService.get_conversation(
            session, 
            uuid.UUID(conversation_id), 
            current_user.id
        )
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        parsed_messages = json.loads(conversation.messages) if conversation.messages else []
        return ConversationDetail(
            id=str(conversation.id),
            title=conversation.title,
            created_at=conversation.created_at.isoformat(),
            updated_at=conversation.updated_at.isoformat(),
            messages=parsed_messages
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import logging
        logging.error(f"Error getting conversation detail: {str(e)}")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving conversation details"
        )