"""
MCP (Model Context Protocol) Server for Todo AI Chatbot
Exposes task operations as tools for AI agents to use
"""

import asyncio
from typing import Dict, Any, List
from mcp.server import Server
from mcp.types import TextContent, Tool, ToolCallResult
from pydantic import BaseModel, Field
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
server = Server("todo-mcp-server")


# Pydantic models for request/response
class TaskCreateRequest(BaseModel):
    title: str
    description: str = ""
    user_id: str


class TaskUpdateRequest(BaseModel):
    task_id: int
    title: str = None
    description: str = None
    completed: bool = None
    user_id: str


class TaskToggleCompleteRequest(BaseModel):
    task_id: int
    user_id: str


class TaskDeleteRequest(BaseModel):
    task_id: int
    user_id: str


class ListTasksRequest(BaseModel):
    user_id: str
    completed: bool = None  # None = all, True = completed, False = pending


# Mock database for demonstration (in production, this would connect to actual database)
mock_tasks_db: Dict[int, Dict[str, Any]] = {}
next_task_id = 1


async def get_next_task_id():
    global next_task_id
    current_id = next_task_id
    next_task_id += 1
    return current_id


async def initialize_mock_db():
    """Initialize mock database with sample data"""
    global mock_tasks_db
    mock_tasks_db = {
        1: {
            "id": 1,
            "user_id": "user-demo",
            "title": "Sample task",
            "description": "This is a sample task for demonstration",
            "completed": False,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    }


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

    task_id = await get_next_task_id()
    task_data = {
        "id": task_id,
        "user_id": user_id,
        "title": title,
        "description": description,
        "completed": False,
        "created_at": "2024-01-01T00:00:00",  # In real implementation, use current timestamp
        "updated_at": "2024-01-01T00:00:00"
    }

    mock_tasks_db[task_id] = task_data

    result = {
        "success": True,
        "task_id": task_id,
        "message": f"Task '{title}' has been added successfully"
    }

    logger.info(f"Task added with ID {task_id}")
    return ToolCallResult(content=[TextContent(type="text", text=str(result))])


@server.tool("list_tasks")
async def list_tasks(
    user_id: str = Field(description="ID of the user whose tasks to list"),
    completed: bool = Field(None, description="Filter by completion status (true=pending, false=completed, null=all)")
) -> ToolCallResult:
    """
    List all tasks for a user with optional filtering.
    """
    logger.info(f"Listing tasks for user {user_id}, completed={completed}")

    user_tasks = [task for task in mock_tasks_db.values() if task["user_id"] == user_id]

    if completed is not None:
        user_tasks = [task for task in user_tasks if task["completed"] == completed]

    result = {
        "tasks": user_tasks,
        "count": len(user_tasks)
    }

    logger.info(f"Found {len(user_tasks)} tasks for user {user_id}")
    return ToolCallResult(content=[TextContent(type="text", text=str(result))])


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

    if task_id not in mock_tasks_db:
        error_result = {
            "success": False,
            "message": f"Task with ID {task_id} not found"
        }
        logger.warning(f"Attempted to update non-existent task {task_id}")
        return ToolCallResult(content=[TextContent(type="text", text=str(error_result))])

    task = mock_tasks_db[task_id]
    if task["user_id"] != user_id:
        error_result = {
            "success": False,
            "message": "Unauthorized: You don't own this task"
        }
        logger.warning(f"User {user_id} attempted to update task {task_id} they don't own")
        return ToolCallResult(content=[TextContent(type="text", text=str(error_result))])

    # Update the task
    if title is not None:
        task["title"] = title
    if description is not None:
        task["description"] = description
    if completed is not None:
        task["completed"] = completed
    task["updated_at"] = "2024-01-01T00:00:00"  # In real implementation, use current timestamp

    result = {
        "success": True,
        "task": task,
        "message": f"Task {task_id} updated successfully"
    }

    logger.info(f"Task {task_id} updated successfully")
    return ToolCallResult(content=[TextContent(type="text", text=str(result))])


@server.tool("delete_task")
async def delete_task(
    task_id: int = Field(description="ID of the task to delete"),
    user_id: str = Field(description="ID of the user who owns the task")
) -> ToolCallResult:
    """
    Delete a task for a user.
    """
    logger.info(f"Deleting task {task_id} for user {user_id}")

    if task_id not in mock_tasks_db:
        error_result = {
            "success": False,
            "message": f"Task with ID {task_id} not found"
        }
        logger.warning(f"Attempted to delete non-existent task {task_id}")
        return ToolCallResult(content=[TextContent(type="text", text=str(error_result))])

    task = mock_tasks_db[task_id]
    if task["user_id"] != user_id:
        error_result = {
            "success": False,
            "message": "Unauthorized: You don't own this task"
        }
        logger.warning(f"User {user_id} attempted to delete task {task_id} they don't own")
        return ToolCallResult(content=[TextContent(type="text", text=str(error_result))])

    del mock_tasks_db[task_id]

    result = {
        "success": True,
        "message": f"Task {task_id} deleted successfully"
    }

    logger.info(f"Task {task_id} deleted successfully")
    return ToolCallResult(content=[TextContent(type="text", text=str(result))])


@server.tool("toggle_task_completion")
async def toggle_task_completion(
    task_id: int = Field(description="ID of the task to toggle"),
    user_id: str = Field(description="ID of the user who owns the task")
) -> ToolCallResult:
    """
    Toggle the completion status of a task for a user.
    """
    logger.info(f"Toggling completion for task {task_id} for user {user_id}")

    if task_id not in mock_tasks_db:
        error_result = {
            "success": False,
            "message": f"Task with ID {task_id} not found"
        }
        logger.warning(f"Attempted to toggle non-existent task {task_id}")
        return ToolCallResult(content=[TextContent(type="text", text=str(error_result))])

    task = mock_tasks_db[task_id]
    if task["user_id"] != user_id:
        error_result = {
            "success": False,
            "message": "Unauthorized: You don't own this task"
        }
        logger.warning(f"User {user_id} attempted to toggle task {task_id} they don't own")
        return ToolCallResult(content=[TextContent(type="text", text=str(error_result))])

    task["completed"] = not task["completed"]
    task["updated_at"] = "2024-01-01T00:00:00"  # In real implementation, use current timestamp

    result = {
        "success": True,
        "task": task,
        "message": f"Task {task_id} completion status toggled to {task['completed']}"
    }

    logger.info(f"Task {task_id} completion status toggled to {task['completed']}")
    return ToolCallResult(content=[TextContent(type="text", text=str(result))])


# Initialize mock database on startup
async def startup():
    await initialize_mock_db()


# Register the startup function
server.on_startup(startup)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # Run as MCP server
        from mcp.server import run_server
        run_server(server)
    else:
        # For testing purposes
        print("MCP Server initialized. Use with MCP client or run with --mcp flag.")