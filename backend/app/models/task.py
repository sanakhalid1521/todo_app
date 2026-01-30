"""Task database model using SQLModel."""

from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.types import Enum as SQLEnum
from typing import Optional
from datetime import datetime, timezone
from app.models.user import User
import enum


class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Category(str, enum.Enum):
    WORK = "work"
    PERSONAL = "personal"
    SHOPPING = "shopping"
    HEALTH = "health"
    OTHER = "other"


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
        index=True,  # Index for search
        description="Task title (3-100 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional task details"
    )
    completed: bool = Field(
        default=False,
        index=True,  # Index for filters
        description="Task completion status"
    )

    # NEW FIELDS
    category: Category = Field(
        default=Category.OTHER,
        sa_column=Column(SQLEnum(Category)),
        description="Task category for organization"
    )
    priority: Priority = Field(
        default=Priority.MEDIUM,
        sa_column=Column(SQLEnum(Priority)),
        description="Task priority level"
    )
    due_date: Optional[datetime] = Field(
        default=None,
        index=True,  # Index for due date filtering
        description="Task due date"
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        index=True,  # Index for sorting
        description="Task creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        index=True,  # Index for sorting
        description="Last modification timestamp"
    )
