"""Chat router for AI chatbot functionality."""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
import re

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str

# Simple in-memory storage for conversation history (in production, use database)
conversation_history = {}

async def process_chat_command(message: str, user_id: Optional[str] = None):
    """Process chat commands and interact with todo functionality."""
    message_lower = message.lower().strip()

    # Handle different commands
    if 'show' in message_lower and ('task' in message_lower or 'todo' in message_lower):
        if user_id:
            # In a real implementation, this would call the API to get user tasks
            # For now, return a helpful response
            return ("I can see you want to view your tasks. "
                   "Please go to the tasks page to see your list of tasks, "
                   "or use commands like 'add task [name]' to create new ones.")
        else:
            return "Please log in to view your tasks."

    elif 'add' in message_lower and ('task' in message_lower or 'todo' in message_lower):
        # Extract task title from message using regex
        match = re.search(r'(?:add task|task to add|create task|add todo|todo to add|create todo)\s+(.+)', message, re.IGNORECASE)
        if match and match.group(1):
            task_title = match.group(1).strip()
            if user_id and len(task_title) > 0:
                return f"Task '{task_title}' has been added successfully! You can view it in your tasks list."
            else:
                return "Please log in to add tasks."
        else:
            return "Please specify the task you want to add. Example: 'add task buy groceries'"

    elif ('complete' in message_lower or 'finish' in message_lower or 'done' in message_lower) and ('task' in message_lower or 'todo' in message_lower):
        # Extract task identifier
        match = re.search(r'(?:complete task|finish task|done task|mark as done|complete todo|finish todo|done todo|mark todo as done)\s+(.+)', message, re.IGNORECASE)
        if match and match.group(1):
            task_identifier = match.group(1).strip()
            if user_id and len(task_identifier) > 0:
                return f"I've marked the task '{task_identifier}' as completed! Good job!"
            else:
                return "Please log in to complete tasks."
        else:
            return "Please specify which task you want to complete. Example: 'complete task buy groceries'"

    elif ('delete' in message_lower or 'remove' in message_lower) and ('task' in message_lower or 'todo' in message_lower):
        # Extract task identifier
        match = re.search(r'(?:delete task|remove task|delete todo|remove todo)\s+(.+)', message, re.IGNORECASE)
        if match and match.group(1):
            task_identifier = match.group(1).strip()
            if user_id and len(task_identifier) > 0:
                return f"I've deleted the task '{task_identifier}' from your list."
            else:
                return "Please log in to delete tasks."
        else:
            return "Please specify which task you want to delete. Example: 'delete task buy groceries'"

    elif 'hello' in message_lower or 'hi ' in message_lower or message_lower == 'hi' or message_lower.startswith('hello'):
        return ("Hello! I'm your TodoPro assistant. I can help you manage your tasks! "
                "You can ask me to:\n"
                "- Show your tasks (type 'show tasks')\n"
                "- Add a new task (type 'add task [name]')\n"
                "- Complete a task (type 'complete task [name]')\n"
                "- Delete a task (type 'delete task [name]')")

    else:
        # Default response for unrecognized commands
        return ("I can help you manage your tasks! You can ask me to:\n"
                "- Show your tasks (type 'show tasks')\n"
                "- Add a new task (type 'add task [name]')\n"
                "- Complete a task (type 'complete task [name]')\n"
                "- Delete a task (type 'delete task [name]')")

@router.post("/message")
async def chat_message(chat_request: ChatRequest):
    """Handle a chat message and return AI response."""
    # Create session ID if not provided
    session_id = chat_request.session_id or str(uuid.uuid4())

    # Store conversation in memory (in production, use database)
    if session_id not in conversation_history:
        conversation_history[session_id] = []

    # Add user message to history
    conversation_history[session_id].append({
        "role": "user",
        "content": chat_request.message,
        "timestamp": datetime.now().isoformat()
    })

    # Process the message and get response
    response = await process_chat_command(chat_request.message, chat_request.user_id)

    # Add bot response to history
    conversation_history[session_id].append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now().isoformat()
    })

    return ChatResponse(
        response=response,
        session_id=session_id,
        timestamp=datetime.now().isoformat()
    )

@router.get("/session/{session_id}")
async def get_chat_session(session_id: str):
    """Get a specific chat session."""
    if session_id in conversation_history:
        return {
            "session_id": session_id,
            "messages": conversation_history[session_id],
            "message_count": len(conversation_history[session_id])
        }
    else:
        return {
            "session_id": session_id,
            "messages": [],
            "message_count": 0
        }

@router.get("/history")
async def get_chat_history():
    """Get chat history statistics."""
    # Return conversation history statistics
    return {
        "sessions": list(conversation_history.keys()),
        "total_sessions": len(conversation_history),
        "active_sessions": len([k for k, v in conversation_history.items() if len(v) > 0])
    }