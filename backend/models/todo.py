"""Todo SQLModel for database persistence."""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Todo(SQLModel, table=True):
    """Todo model representing a task in the database."""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=5, max_length=500)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def update_timestamps(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def toggle_complete(self) -> None:
        """Toggle the completed status."""
        self.completed = not self.completed
        self.update_timestamps()
