#!/usr/bin/env python3
"""Basic test to verify that the application works."""

def test_basic_imports():
    """Test basic imports work."""
    print("Testing basic imports...")

    # Test main app
    from main import app
    print("SUCCESS: Main app imported successfully")

    # Test database
    from database import async_engine, get_async_session
    print("SUCCESS: Database components imported successfully")

    # Test models
    from app.models.task import Task
    print("SUCCESS: Task model imported successfully")

    from app.models.user import User
    print("SUCCESS: User model imported successfully")

    from app.models.conversation import ConversationMessage, ConversationSession
    print("SUCCESS: Conversation models imported successfully")

    # Test agents
    from app.agents.todo_agent import TodoAgent
    print("SUCCESS: TodoAgent imported successfully")

    # Test routers
    from app.routers.tasks import router as tasks_router
    print("SUCCESS: Tasks router imported successfully")

    from app.routers.chat import router as chat_router
    print("SUCCESS: Chat router imported successfully")

    print("\nAll basic imports successful! Application structure is working.")

if __name__ == "__main__":
    test_basic_imports()