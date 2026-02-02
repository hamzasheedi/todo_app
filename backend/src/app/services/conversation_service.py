"""
Conversation Service
Handles conversation management and persistence
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlmodel import Session, select
from ..models.conversation import Conversation
from ..models.mcp_invocation import MCPToolInvocation
import uuid
import json


class ConversationService:
    """Service class for managing conversations"""

    @staticmethod
    def get_conversation(session: Session, conversation_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Conversation]:
        """Retrieve a specific conversation for a user"""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        return session.exec(statement).first()

    @staticmethod
    def create_conversation(session: Session, user_id: uuid.UUID, title: Optional[str] = None) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation(
            user_id=user_id,
            title=title,
            messages=json.dumps([])
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def update_conversation(session: Session, conversation: Conversation) -> Conversation:
        """Update an existing conversation"""
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def add_message_to_conversation(session: Session, conversation_id: uuid.UUID, role: str, content: str) -> Conversation:
        """Add a message to an existing conversation"""
        conversation = session.get(Conversation, conversation_id)
        if conversation:
            # Get existing messages or initialize as empty list
            messages = json.loads(conversation.messages) if conversation.messages else []

            message = {
                "id": str(uuid.uuid4()),
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow().isoformat()
            }
            messages.append(message)

            conversation.messages = json.dumps(messages)
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
        return conversation

    @staticmethod
    def get_user_conversations(session: Session, user_id: uuid.UUID) -> List[Conversation]:
        """Retrieve all conversations for a user"""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return session.exec(statement).all()