"""
Real MCP (Model Context Protocol) Server for Todo AI Chatbot
Exposes task operations as tools for AI agents to use with actual database connection
"""

import asyncio
from typing import Dict, Any, List
from mcp.server import Server
from mcp.types import TextContent, ToolCallResult
from pydantic import BaseModel, Field
import logging
from sqlmodel import create_engine, Session, select
from datetime import datetime
import hashlib
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
server = Server("todo-mcp-server")

# Database setup - connecting to the existing database
from app.database import engine
from app.models.task import Task  # Using the Task model with user_id

# Helper function to convert UUID to numeric ID (mirroring the backend logic from tasks.py)
def get_numeric_id(uuid_str: str) -> int:
    """Convert UUID to a consistent numeric ID."""
    # Use a hash of the UUID to generate a consistent numeric ID
    hash_obj = hashlib.md5(uuid_str.encode())
    hex_dig = hash_obj.hexdigest()
    # Convert first 8 hex characters to int and keep within range
    return int(hex_dig[:8], 16) % 10000000

def get_uuid_from_numeric_id(numeric_id: int, tasks) -> str:
    """Find the UUID corresponding to a numeric ID by checking all tasks."""
    for task in tasks:
        if get_numeric_id(task.id) == numeric_id:
            return task.id
    return None

# MCP Tool Definitions
@server.tool("add_task")
async def add_task(
    title: str = Field(description="The title of the task to add"),
    description: str = Field("", description="Description of the task"),
    user_id: str = Field(description="ID of the user adding the task")
) -> ToolCallResult:
    """
    Add a new task for a user.
    """
    logger.info(f"Adding task for user {user_id}: {title}")

    try:
        # Create a new task in the database
        with Session(engine) as session:
            # Create the task object using the Task model with user_id
            new_task = Task(
                title=title,
                description=description or "",
                completed=False,
                user_id=user_id
            )

            session.add(new_task)
            session.commit()
            session.refresh(new_task)

            # Convert to the expected format with numeric ID
            # Since Task model uses integer ID directly, we can use it as is
            result = {
                "success": True,
                "task_id": new_task.id,
                "message": f"Task '{title}' has been added successfully"
            }

        logger.info(f"Task added with ID {new_task.id}")
        return ToolCallResult(content=[TextContent(type="text", text=str(result))])
    except Exception as e:
        error_result = {
            "success": False,
            "message": f"Error adding task: {str(e)}"
        }
        logger.error(f"Error adding task: {str(e)}")
        return ToolCallResult(content=[TextContent(type="text", text=str(error_result))])


@server.tool("list_tasks")
async def list_tasks(
    user_id: str = Field(description="ID of the user whose tasks to list"),
    completed: bool = Field(None, description="Filter by completion status (true=completed, false=not completed, null=all)")
) -> ToolCallResult:
    """
    List all tasks for a user with optional filtering.
    """
    logger.info(f"Listing tasks for user {user_id}, completed={completed}")

    try:
        # Query the database for user's tasks
        with Session(engine) as session:
            # Query tasks for the specific user
            query = select(Task).where(Task.user_id == user_id)

            if completed is not None:
                query = query.where(Task.completed == completed)

            tasks = session.exec(query).all()

            # Convert to the expected format
            task_list = []
            for task in tasks:
                task_data = {
                    "id": task.id,
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat(),
                }
                task_list.append(task_data)

            result = {
                "tasks": task_list,
                "count": len(task_list),
                "message": f"Found {len(task_list)} tasks"
            }

            logger.info(f"Found {len(task_list)} tasks for user {user_id}")
            return ToolCallResult(content=[TextContent(type="text", text=str(result))])
    except Exception as e:
        error_result = {
            "success": False,
            "message": f"Error listing tasks: {str(e)}"
        }
        logger.error(f"Error listing tasks: {str(e)}")
        return ToolCallResult(content=[TextContent(type="text", text=str(error_result))])


@server.tool("update_task")
async def update_task(
    task_id: int = Field(description="ID of the task to update"),
    title: str = Field(None, description="New title for the task"),
    description: str = Field(None, description="New description for the task"),
    completed: bool = Field(None, description="New completion status for the task"),
    user_id: str = Field(description="ID of the user who owns the task")
) -> ToolCallResult:
    """
    Update an existing task for a user.
    """
    logger.info(f"Updating task {task_id} for user {user_id}")

    try:
        # Find the task by ID
        with Session(engine) as session:
            # Get the task by ID and user_id to ensure ownership
            query = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
            target_task = session.exec(query).first()

            if not target_task:
                error_result = {
                    "success": False,
                    "message": f"Task with ID {task_id} not found or you don't have permission to modify it"
                }
                logger.warning(f"Attempted to update non-existent or unauthorized task {task_id}")
                return ToolCallResult(content=[TextContent(type="text", text=str(error_result))])

            # Update the task fields if provided
            if title is not None:
                target_task.title = title
            if description is not None:
                target_task.description = description
            if completed is not None:
                target_task.completed = completed
            target_task.updated_at = datetime.now()

            session.add(target_task)
            session.commit()
            session.refresh(target_task)

            # Convert to expected format
            result = {
                "success": True,
                "task": {
                    "id": target_task.id,
                    "user_id": target_task.user_id,
                    "title": target_task.title,
                    "description": target_task.description,
                    "completed": target_task.completed,
                    "created_at": target_task.created_at.isoformat(),
                    "updated_at": target_task.updated_at.isoformat(),
                },
                "message": f"Task {task_id} updated successfully"
            }

            logger.info(f"Task {task_id} updated successfully")
            return ToolCallResult(content=[TextContent(type="text", text=str(result))])
    except Exception as e:
        error_result = {
            "success": False,
            "message": f"Error updating task: {str(e)}"
        }
        logger.error(f"Error updating task: {str(e)}")
        return ToolCallResult(content=[TextContent(type="text", text=str(error_result))])


@server.tool("delete_task")
async def delete_task(
    task_id: int = Field(description="ID of the task to delete"),
    user_id: str = Field(description="ID of the user who owns the task")
) -> ToolCallResult:
    """
    Delete a task for a user.
    """
    logger.info(f"Deleting task {task_id} for user {user_id}")

    try:
        # Find the task by ID and user_id to ensure ownership
        with Session(engine) as session:
            query = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
            target_task = session.exec(query).first()

            if not target_task:
                error_result = {
                    "success": False,
                    "message": f"Task with ID {task_id} not found or you don't have permission to delete it"
                }
                logger.warning(f"Attempted to delete non-existent or unauthorized task {task_id}")
                return ToolCallResult(content=[TextContent(type="text", text=str(error_result))])

            session.delete(target_task)
            session.commit()

            result = {
                "success": True,
                "message": f"Task {task_id} deleted successfully"
            }

            logger.info(f"Task {task_id} deleted successfully")
            return ToolCallResult(content=[TextContent(type="text", text=str(result))])
    except Exception as e:
        error_result = {
            "success": False,
            "message": f"Error deleting task: {str(e)}"
        }
        logger.error(f"Error deleting task: {str(e)}")
        return ToolCallResult(content=[TextContent(type="text", text=str(error_result))])


@server.tool("toggle_task_completion")
async def toggle_task_completion(
    task_id: int = Field(description="ID of the task to toggle"),
    user_id: str = Field(description="ID of the user who owns the task")
) -> ToolCallResult:
    """
    Toggle the completion status of a task for a user.
    """
    logger.info(f"Toggling completion for task {task_id} for user {user_id}")

    try:
        # Find the task by ID and user_id to ensure ownership
        with Session(engine) as session:
            query = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
            target_task = session.exec(query).first()

            if not target_task:
                error_result = {
                    "success": False,
                    "message": f"Task with ID {task_id} not found or you don't have permission to modify it"
                }
                logger.warning(f"Attempted to toggle non-existent or unauthorized task {task_id}")
                return ToolCallResult(content=[TextContent(type="text", text=str(error_result))])

            # Toggle completion status
            target_task.completed = not target_task.completed
            target_task.updated_at = datetime.now()

            session.add(target_task)
            session.commit()
            session.refresh(target_task)

            # Convert to expected format
            result = {
                "success": True,
                "task": {
                    "id": target_task.id,
                    "user_id": target_task.user_id,
                    "title": target_task.title,
                    "description": target_task.description,
                    "completed": target_task.completed,
                    "created_at": target_task.created_at.isoformat(),
                    "updated_at": target_task.updated_at.isoformat(),
                },
                "message": f"Task {task_id} completion status toggled to {target_task.completed}"
            }

            logger.info(f"Task {task_id} completion status toggled to {target_task.completed}")
            return ToolCallResult(content=[TextContent(type="text", text=str(result))])
    except Exception as e:
        error_result = {
            "success": False,
            "message": f"Error toggling task completion: {str(e)}"
        }
        logger.error(f"Error toggling task completion: {str(e)}")
        return ToolCallResult(content=[TextContent(type="text", text=str(error_result))])


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # Run as MCP server
        from mcp.server import run_server
        run_server(server)
    else:
        # For testing purposes
        print("MCP Server initialized. Use with MCP client or run with --mcp flag.")