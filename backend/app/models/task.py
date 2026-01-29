"""Task database model using SQLModel."""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone


class Task(SQLModel, table=True):
    """Task entity linked to a user."""

    __tablename__ = "tasks"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Auto-increment task ID"
    )
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        description="Owning user UUID"
    )
    title: str = Field(
        max_length=100,
        description="Task title (3-100 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional task details"
    )
    completed: bool = Field(
        default=False,
        description="Task completion status"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        description="Task creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        description="Last modification timestamp"
    )
