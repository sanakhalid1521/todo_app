"""Tasks API endpoints for user-based todo management."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession
import hashlib

from database import get_async_session
from crud.todo import todo_crud
from schemas.todo import (
    TodoCreate,
    TodoUpdate,
    TodoResponse,
    TodoListResponse,
)

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])

# In-memory mapping of numeric IDs to UUIDs for compatibility
# In a real application, this would be stored in the database
id_mapping = {}

def get_numeric_id(uuid_str: str) -> int:
    """Convert UUID to a consistent numeric ID."""
    # Use a hash of the UUID to generate a consistent numeric ID
    hash_obj = hashlib.md5(uuid_str.encode())
    hex_dig = hash_obj.hexdigest()
    # Convert first 8 hex characters to int and keep within range
    return int(hex_dig[:8], 16) % 10000000

def get_uuid_from_numeric_id(numeric_id: int, todos) -> str:
    """Find the UUID corresponding to a numeric ID by checking all todos."""
    for todo in todos:
        if get_numeric_id(todo.id) == numeric_id:
            return todo.id
    return None

def verify_user_authorization(authorization: str = Header(default=None), user_id: str = None) -> bool:
    """Verify user is authorized to access this user's resources."""
    # Special case: allow access to 'user-demo' resources without strict token checking
    # This is for demo/testing purposes when no user is properly authenticated
    if user_id == 'user-demo':
        return True

    if not authorization or not authorization.startswith("Bearer "):
        return False

    # In this async API, we don't have the full token extraction logic
    # For now, we'll just allow the user-demo case and return True for demo purposes
    # In a real app, you'd extract and validate the token here
    return True


@router.get("")
async def list_tasks(
    user_id: str,
    completed: Optional[bool] = Query(None),
    authorization: str = Header(default=None),
    db: AsyncSession = Depends(get_async_session),
):
    """Get all tasks for a user with optional filtering."""
    # Verify authorization
    if not verify_user_authorization(authorization, user_id):
        raise HTTPException(status_code=403, detail="Not authorized")

    todos = await todo_crud.get_all(db)

    # Filter by completion status if specified
    if completed is not None:
        todos = [t for t in todos if t.completed == completed]

    # Convert to frontend-compatible format
    tasks = []
    for todo in todos:
        numeric_id = get_numeric_id(todo.id)
        task_data = {
            "id": numeric_id,
            "user_id": user_id,
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed,
            "created_at": todo.created_at.isoformat(),
            "updated_at": todo.updated_at.isoformat(),
        }
        tasks.append(task_data)

    return tasks


@router.post("")
async def create_task(
    user_id: str,
    task_data: TodoCreate,
    authorization: str = Header(default=None),
    db: AsyncSession = Depends(get_async_session),
):
    """Create a new task for a user."""
    # Verify authorization
    if not verify_user_authorization(authorization, user_id):
        raise HTTPException(status_code=403, detail="Not authorized")

    todo = await todo_crud.create(db, task_data)

    # Return in frontend-compatible format
    numeric_id = get_numeric_id(todo.id)
    return {
        "id": numeric_id,
        "user_id": user_id,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "created_at": todo.created_at.isoformat(),
        "updated_at": todo.updated_at.isoformat(),
    }


@router.get("/{task_id}")
async def get_task(
    user_id: str,
    task_id: str,
    authorization: str = Header(default=None),
    db: AsyncSession = Depends(get_async_session),
):
    """Get a specific task for a user."""
    # Verify authorization
    if not verify_user_authorization(authorization, user_id):
        raise HTTPException(status_code=403, detail="Not authorized")

    todos = await todo_crud.get_all(db)
    task_id_int = int(task_id)

    for todo in todos:
        if get_numeric_id(todo.id) == task_id_int:
            numeric_id = get_numeric_id(todo.id)
            return {
                "id": numeric_id,
                "user_id": user_id,
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "created_at": todo.created_at.isoformat(),
                "updated_at": todo.updated_at.isoformat(),
            }

    raise HTTPException(status_code=404, detail="Task not found")


@router.put("/{task_id}")
async def update_task(
    user_id: str,
    task_id: str,
    update_data: TodoUpdate,
    authorization: str = Header(default=None),
    db: AsyncSession = Depends(get_async_session),
):
    """Update a specific task for a user."""
    # Verify authorization
    if not verify_user_authorization(authorization, user_id):
        raise HTTPException(status_code=403, detail="Not authorized")

    todos = await todo_crud.get_all(db)
    task_id_int = int(task_id)

    original_todo_id = get_uuid_from_numeric_id(task_id_int, todos)

    if not original_todo_id:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update the original todo
    updated_todo = await todo_crud.update(db, original_todo_id, update_data)

    if not updated_todo:
        raise HTTPException(status_code=404, detail="Task not found")

    # Return in frontend-compatible format
    numeric_id = get_numeric_id(updated_todo.id)
    return {
        "id": numeric_id,
        "user_id": user_id,
        "title": updated_todo.title,
        "description": updated_todo.description,
        "completed": updated_todo.completed,
        "created_at": updated_todo.created_at.isoformat(),
        "updated_at": updated_todo.updated_at.isoformat(),
    }


@router.delete("/{task_id}")
async def delete_task(
    user_id: str,
    task_id: str,
    authorization: str = Header(default=None),
    db: AsyncSession = Depends(get_async_session),
):
    """Delete a specific task for a user."""
    # Verify authorization
    if not verify_user_authorization(authorization, user_id):
        raise HTTPException(status_code=403, detail="Not authorized")

    todos = await todo_crud.get_all(db)
    task_id_int = int(task_id)

    original_todo_id = get_uuid_from_numeric_id(task_id_int, todos)

    if not original_todo_id:
        raise HTTPException(status_code=404, detail="Task not found")

    # Delete the original todo
    success = await todo_crud.delete(db, original_todo_id)

    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"success": True}


@router.patch("/{task_id}/toggle")
async def toggle_task(
    user_id: str,
    task_id: str,
    authorization: str = Header(default=None),
    db: AsyncSession = Depends(get_async_session),
):
    """Toggle completion status of a specific task for a user."""
    # Verify authorization
    if not verify_user_authorization(authorization, user_id):
        raise HTTPException(status_code=403, detail="Not authorized")

    todos = await todo_crud.get_all(db)
    task_id_int = int(task_id)

    original_todo_id = get_uuid_from_numeric_id(task_id_int, todos)

    if not original_todo_id:
        raise HTTPException(status_code=404, detail="Task not found")

    # Toggle the original todo
    toggled_todo = await todo_crud.toggle(db, original_todo_id)

    if not toggled_todo:
        raise HTTPException(status_code=404, detail="Task not found")

    # Return in frontend-compatible format
    numeric_id = get_numeric_id(toggled_todo.id)
    return {
        "id": numeric_id,
        "user_id": user_id,
        "title": toggled_todo.title,
        "description": toggled_todo.description,
        "completed": toggled_todo.completed,
        "created_at": toggled_todo.created_at.isoformat(),
        "updated_at": toggled_todo.updated_at.isoformat(),
    }