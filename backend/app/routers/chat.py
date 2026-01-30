"""Chat router for AI chatbot functionality using MCP and OpenAI Agents SDK."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.services.conversations import ConversationService
from app.models.conversation import ConversationRole
from app.agents.todo_agent import todo_agent

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str

class Message(BaseModel):
    role: str
    content: str

class ChatSessionResponse(BaseModel):
    session_id: str
    messages: List[Message]
    message_count: int

@router.post("/message")
async def chat_message(
    chat_request: ChatRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """Handle a chat message and return AI response using MCP tools."""
    # Validate user_id
    if not chat_request.user_id:
        user_id = "user-demo"  # Default user for demo purposes
    else:
        user_id = chat_request.user_id

    # Get or create session ID
    session_id = chat_request.session_id or str(uuid.uuid4())

    # Create or get conversation session
    conversation_session = await ConversationService.get_conversation_session(db, session_id)
    if not conversation_session:
        conversation_session = await ConversationService.create_conversation_session(
            db, user_id, f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )

    # Add user message to conversation
    await ConversationService.add_message_to_conversation(
        db, session_id, ConversationRole.USER, chat_request.message
    )

    # Get conversation history for context
    messages = await ConversationService.get_conversation_messages(db, session_id)
    conversation_context = [
        {"role": msg.role.value, "content": msg.content}
        for msg in messages
    ]

    try:
        # Process the message using the OpenAI agent with MCP tools
        ai_response = await todo_agent.process_message(
            message=chat_request.message,
            user_id=user_id,
            conversation_history=conversation_context
        )

        # Add assistant response to conversation
        await ConversationService.add_message_to_conversation(
            db, session_id, ConversationRole.ASSISTANT, ai_response
        )

        return ChatResponse(
            response=ai_response,
            session_id=session_id,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        # Handle errors gracefully
        error_response = f"Sorry, I encountered an error processing your request: {str(e)}"

        # Add error response to conversation
        await ConversationService.add_message_to_conversation(
            db, session_id, ConversationRole.ASSISTANT, error_response
        )

        return ChatResponse(
            response=error_response,
            session_id=session_id,
            timestamp=datetime.now().isoformat()
        )

@router.get("/session/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: str,
    db: AsyncSession = Depends(get_async_session)
):
    """Get a specific chat session."""
    messages = await ConversationService.get_conversation_messages(db, session_id)

    chat_messages = [
        Message(role=msg.role.value, content=msg.content)
        for msg in messages
    ]

    return ChatSessionResponse(
        session_id=session_id,
        messages=chat_messages,
        message_count=len(chat_messages)
    )

@router.get("/history")
async def get_chat_history(
    user_id: str,
    db: AsyncSession = Depends(get_async_session)
):
    """Get chat history for a user."""
    user_sessions = await ConversationService.get_user_conversations(db, user_id)

    return {
        "sessions": [
            {
                "session_id": session.session_id,
                "title": session.title,
                "created_at": session.created_at.isoformat(),
                "updated_at": session.updated_at.isoformat()
            }
            for session in user_sessions
        ],
        "total_sessions": len(user_sessions)
    }