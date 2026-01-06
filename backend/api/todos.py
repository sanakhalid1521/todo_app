"""Todo API endpoints."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from ..crud.todo import todo_crud
from ..schemas.todo import (
    TodoCreate,
    TodoUpdate,
    TodoResponse,
    TodoListResponse,
)

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=TodoResponse, status_code=201)
async def create_todo(
    todo_data: TodoCreate,
    db: AsyncSession = Depends(get_async_session),
):
    """Create a new todo."""
    return await todo_crud.create(db, todo_data)


@router.get("", response_model=TodoListResponse)
async def get_todos(
    completed: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_async_session),
):
    """Get all todos with optional filtering."""
    todos = await todo_crud.get_all(db)

    if completed is not None:
        todos = [t for t in todos if t.completed == completed]

    stats = await todo_crud.get_stats(db)
    return TodoListResponse(
        todos=todos,
        total=stats["total"],
        completed=stats["completed"],
        pending=stats["pending"],
    )


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: str,
    db: AsyncSession = Depends(get_async_session),
):
    """Get a todo by ID."""
    todo = await todo_crud.get_by_id(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: str,
    todo_data: TodoUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """Update a todo."""
    todo = await todo_crud.update(db, todo_id, todo_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: str,
    db: AsyncSession = Depends(get_async_session),
):
    """Delete a todo."""
    success = await todo_crud.delete(db, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return None


@router.post("/{todo_id}/toggle", response_model=TodoResponse)
async def toggle_todo(
    todo_id: str,
    db: AsyncSession = Depends(get_async_session),
):
    """Toggle todo completed status."""
    todo = await todo_crud.toggle(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
