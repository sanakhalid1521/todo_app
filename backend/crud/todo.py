"""Todo CRUD operations."""
from typing import Optional

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.todo import Todo
from schemas.todo import TodoCreate, TodoUpdate


class TodoCRUD:
    """CRUD operations for Todo model."""

    async def create(self, db: AsyncSession, todo_data: TodoCreate) -> Todo:
        """Create a new todo."""
        todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
        )
        db.add(todo)
        await db.commit()
        await db.refresh(todo)
        return todo

    async def get_all(self, db: AsyncSession) -> list[Todo]:
        """Get all todos."""
        result = await db.execute(select(Todo).order_by(Todo.created_at.desc()))
        return list(result.scalars().all())

    async def get_by_id(self, db: AsyncSession, todo_id: str) -> Optional[Todo]:
        """Get a todo by ID."""
        result = await db.execute(select(Todo).where(Todo.id == todo_id))
        return result.scalar_one_or_none()

    async def update(
        self, db: AsyncSession, todo_id: str, todo_data: TodoUpdate
    ) -> Optional[Todo]:
        """Update a todo."""
        todo = await self.get_by_id(db, todo_id)
        if not todo:
            return None

        update_data = todo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo, field, value)
        todo.update_timestamps()

        await db.commit()
        await db.refresh(todo)
        return todo

    async def delete(self, db: AsyncSession, todo_id: str) -> bool:
        """Delete a todo."""
        todo = await self.get_by_id(db, todo_id)
        if not todo:
            return False

        await db.delete(todo)
        await db.commit()
        return True

    async def toggle(self, db: AsyncSession, todo_id: str) -> Optional[Todo]:
        """Toggle todo completed status."""
        todo = await self.get_by_id(db, todo_id)
        if not todo:
            return None

        todo.toggle_complete()
        await db.commit()
        await db.refresh(todo)
        return todo

    async def get_stats(self, db: AsyncSession) -> dict:
        """Get todo statistics."""
        todos = await self.get_all(db)
        total = len(todos)
        completed = sum(1 for t in todos if t.completed)
        pending = total - completed
        return {"total": total, "completed": completed, "pending": pending}


todo_crud = TodoCRUD()
