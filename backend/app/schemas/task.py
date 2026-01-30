"""Task-related Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
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


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    category: Category = Field(default=Category.OTHER)
    priority: Priority = Field(default=Priority.MEDIUM)
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None
    category: Optional[Category] = None
    priority: Optional[Priority] = None
    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    """Schema for task response data."""

    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime
    category: Category
    priority: Priority
    due_date: Optional[datetime] = None

    class Config:
        from_attributes = True
