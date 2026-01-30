"""Pytest configuration and fixtures."""
import os
import sys
from typing import Generator

import pytest

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set environment variables before imports
os.environ["DATABASE_URL"] = "postgresql://neondb_owner:npg_Ge0rDskgW9VF@ep-dry-tree-adewdlhc-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from backend.database import get_async_session
from backend.main import app
from sqlmodel import SQLModel


# Create sync test engine (for TestClient)
test_engine = create_engine(os.environ["DATABASE_URL"], echo=False)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create a fresh database session for each test."""
    # Create tables - use SQLModel's metadata which includes all registered models
    SQLModel.metadata.create_all(bind=test_engine)

    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop tables after test
        SQLModel.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create test client with overridden database session."""

    def override_get_session():
        yield db_session

    app.dependency_overrides[get_async_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_task_data() -> dict:
    """Sample task data for tests."""
    return {
        "user_id": "test-user-1234-5678-abcd-ef1234567890",
        "title": "Buy Milk",
        "description": "Whole milk, 2 liters from the store",
    }


@pytest.fixture
def sample_task_data_with_id() -> dict:
    """Sample task data with ID."""
    return {
        "id": 1,  # Auto-generated int ID for the Task model
        "user_id": "test-user-1234-5678-abcd-ef1234567890",
        "title": "Buy Milk",
        "description": "Whole milk, 2 liters from the store",
        "completed": False,
    }
