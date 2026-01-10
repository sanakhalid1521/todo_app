"""
Services for managing conversation state in Todo AI Chatbot
"""

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.conversation import ConversationMessage, ConversationSession, ConversationRole
from typing import List, Optional
from datetime import datetime


class ConversationService:
    @staticmethod
    async def create_conversation_session(db: AsyncSession, user_id: str, title: str = "New Conversation") -> ConversationSession:
        """Create a new conversation session."""
        session = ConversationSession(
            user_id=user_id,
            title=title
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    @staticmethod
    async def get_conversation_session(db: AsyncSession, session_id: str) -> Optional[ConversationSession]:
        """Get a conversation session by ID."""
        statement = select(ConversationSession).where(ConversationSession.session_id == session_id)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    async def add_message_to_conversation(
        db: AsyncSession,
        session_id: str,
        role: ConversationRole,
        content: str
    ) -> ConversationMessage:
        """Add a message to a conversation."""
        message = ConversationMessage(
            conversation_id=session_id,
            role=role,
            content=content,
            timestamp=datetime.utcnow()
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message

    @staticmethod
    async def get_conversation_messages(db: AsyncSession, session_id: str) -> List[ConversationMessage]:
        """Get all messages for a conversation session."""
        statement = select(ConversationMessage).where(
            ConversationMessage.conversation_id == session_id
        ).order_by(ConversationMessage.timestamp.asc())
        result = await db.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def update_conversation_title(db: AsyncSession, session_id: str, title: str):
        """Update the title of a conversation."""
        statement = select(ConversationSession).where(ConversationSession.session_id == session_id)
        result = await db.execute(statement)
        session = result.scalar_one_or_none()
        if session:
            session.title = title
            session.updated_at = datetime.utcnow()
            db.add(session)
            await db.commit()

    @staticmethod
    async def get_user_conversations(db: AsyncSession, user_id: str) -> List[ConversationSession]:
        """Get all conversations for a user."""
        statement = select(ConversationSession).where(
            ConversationSession.user_id == user_id
        ).order_by(ConversationSession.updated_at.desc())
        result = await db.execute(statement)
        return result.scalars().all()