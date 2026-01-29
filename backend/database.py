"""Database connection and session management."""
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import asyncpg
from dotenv import load_dotenv
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
import logging

# Load environment variables from .env file
load_dotenv(".env")  # Simplified for direct execution

# Database connection string from .env
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback to SQLite for development if no DATABASE_URL is set
    DATABASE_URL = "sqlite:///./todo_dev.db"
    logging.warning("DATABASE_URL not set, using SQLite for development")

# Convert to async URL for appropriate async drivers
if DATABASE_URL.startswith("postgresql://"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("?sslmode=require", "")
elif DATABASE_URL.startswith("sqlite:///"):
    # For SQLite, use aiosqlite driver
    ASYNC_DATABASE_URL = DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
else:
    # For other cases, keep the same URL
    ASYNC_DATABASE_URL = DATABASE_URL

# Import all models so they are registered with SQLModel
from models.todo import Todo
from app.models.task import Task
from app.models.conversation import ConversationMessage, ConversationSession
from app.models.user import User

# Create async engine for SQLModel
if ASYNC_DATABASE_URL.startswith("sqlite+aiosqlite"):
    # For SQLite, use aiosqlite driver
    async_engine = create_async_engine(
        ASYNC_DATABASE_URL,
        echo=True,
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )
else:
    # For PostgreSQL, use asyncpg driver with proper connection settings
    async_engine = create_async_engine(
        ASYNC_DATABASE_URL,
        echo=True,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_timeout=30,
        pool_reset_on_return='commit',
        connect_args={
            "server_settings": {
                "application_name": "todo-app",
            },
            "command_timeout": 60,
        }
    )


async def init_db() -> None:
    """Initialize database tables."""
    print("Initializing database tables...")
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Database tables initialized successfully!")


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session dependency."""
    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        try:
            yield session
        finally:
            await session.close()


async def test_connection() -> bool:
    """Test database connection."""
    try:
        if DATABASE_URL.startswith("postgresql://"):
            # Test PostgreSQL connection
            import asyncpg
            conn = await asyncpg.connect(DATABASE_URL)
            version = await conn.fetchval("SELECT version()")
            await conn.close()
            print("[OK] PostgreSQL database connected successfully!")
            print(f"    PostgreSQL Version: {version}")
        else:
            # Test SQLite connection using SQLAlchemy
            from sqlalchemy import create_engine
            engine = create_engine(DATABASE_URL)
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("[OK] SQLite database connected successfully!")

        return True
    except Exception as e:
        print(f"[FAIL] Database connection failed: {e}")
        return False


@asynccontextmanager
async def get_db_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    """Get raw database connection for direct queries."""
    if DATABASE_URL.startswith("postgresql://"):
        conn = await asyncpg.connect(DATABASE_URL)
        try:
            yield conn
        finally:
            await conn.close()
    else:
        # For SQLite, we can't use asyncpg, so we'll yield None
        # In a real application, you'd need to implement a different approach for SQLite
        yield None
