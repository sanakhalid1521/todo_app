"""Database connection and table creation."""

from sqlmodel import create_engine, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
import asyncio

# Import all models to register them with SQLModel metadata
from models.todo import Todo
from app.models.user import User
from app.models.task import Task
from app.models.conversation import ConversationMessage, ConversationSession

# Create SQLModel engine - use SQLite for local dev
# For PostgreSQL, use: postgresql://user:pass@host/db
sync_engine = create_engine(settings.DATABASE_URL, echo=True)

# Create async engine for async operations - handle different DB types
if settings.DATABASE_URL.startswith("postgresql://"):
    async_database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    # Handle common Neon/PostgreSQL SSL parameters that need to be stripped for asyncpg
    if "?sslmode=require" in async_database_url:
        async_database_url = async_database_url.replace("?sslmode=require", "")
    if "&sslmode=require" in async_database_url:
        async_database_url = async_database_url.replace("&sslmode=require", "")
    if "?sslmode=prefer" in async_database_url:
        async_database_url = async_database_url.replace("?sslmode=prefer", "")
    if "&sslmode=prefer" in async_database_url:
        async_database_url = async_database_url.replace("&sslmode=prefer", "")
    # Remove any remaining query parameters that asyncpg doesn't support
    if "?" in async_database_url and "sslmode" in async_database_url:
        parts = async_database_url.split("?", 1)
        base_url = parts[0]
        params = parts[1].split("&")
        filtered_params = [p for p in params if not p.startswith("ssl")]
        if filtered_params:
            async_database_url = f"{base_url}?{'&'.join(filtered_params)}"
        else:
            async_database_url = base_url
elif settings.DATABASE_URL.startswith("sqlite:///"):
    async_database_url = settings.DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
else:
    async_database_url = settings.DATABASE_URL

async_engine = create_async_engine(async_database_url, echo=True)


def create_tables():
    """Create all database tables from SQLModel metadata."""
    # Ensure all models are imported before creating tables
    from models.todo import Todo
    from app.models.user import User
    from app.models.task import Task
    from app.models.conversation import ConversationMessage, ConversationSession

    SQLModel.metadata.create_all(sync_engine)


def get_engine():
    """Get the database engine."""
    return sync_engine


async def get_async_session():
    """Get async database session generator for dependency injection."""
    async with AsyncSession(async_engine) as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database tables asynchronously."""
    # Ensure all models are imported before initialization
    from models.todo import Todo
    from app.models.user import User
    from app.models.task import Task
    from app.models.conversation import ConversationMessage, ConversationSession

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
