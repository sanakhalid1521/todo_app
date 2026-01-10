"""
Database models for conversation state management in Todo AI Chatbot
"""

from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional
import uuid
from datetime import datetime
from enum import Enum


class ConversationRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class ConversationMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: str = Field(index=True)
    role: ConversationRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConversationSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()), unique=True, index=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    title: Optional[str] = Field(default="New Conversation")