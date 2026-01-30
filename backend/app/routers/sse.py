"""Server-Sent Events router for real-time updates."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlmodel import Session
from app.database import get_engine
from app.models.task import Task
import json
import asyncio
from typing import Generator, Dict, Any

router = APIRouter(tags=["SSE"])

# Global clients set to track connected clients
clients = set()


@router.get("/api/{user_id}/tasks/stream")
async def stream_tasks(user_id: str, request: Request):
    """Stream task updates to connected clients using Server-Sent Events."""

    async def event_generator():
        client_queue = asyncio.Queue()
        clients.add(client_queue)

        # Send initial connection event
        yield f"data: {json.dumps({'event': 'connected', 'user_id': user_id})}\n\n"

        try:
            while True:
                # Check if client disconnected
                if await request.is_disconnected():
                    break

                try:
                    # Wait for task updates (with timeout to check disconnection)
                    task_update = await asyncio.wait_for(client_queue.get(), timeout=30.0)

                    # Send the task update to the client
                    yield f"data: {json.dumps(task_update)}\n\n"

                except asyncio.TimeoutError:
                    # Send heartbeat to keep connection alive
                    yield f"data: {json.dumps({'event': 'heartbeat'})}\n\n"
                    continue

        except Exception as e:
            print(f"SSE connection error for user {user_id}: {str(e)}")
        finally:
            # Remove client when connection closes
            if client_queue in clients:
                clients.remove(client_queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


def broadcast_task_update(update_data: Dict[str, Any]):
    """Broadcast a task update to all connected clients."""
    for client_queue in clients.copy():
        try:
            client_queue.put_nowait(update_data)
        except Exception as e:
            print(f"Error broadcasting to client: {e}")
            # Remove problematic client
            if client_queue in clients:
                clients.remove(client_queue)


def broadcast_task_event(event_type: str, task: Task, user_id: str):
    """Broadcast a specific task event to clients."""
    update_data = {
        "event": event_type,
        "task": {
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "category": task.category.value if hasattr(task.category, 'value') else task.category,
            "priority": task.priority.value if hasattr(task.priority, 'value') else task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        },
        "timestamp": task.updated_at.isoformat()
    }
    broadcast_task_update(update_data)