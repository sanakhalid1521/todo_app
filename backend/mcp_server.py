#!/usr/bin/env python3
"""
Standalone MCP (Model Context Protocol) Server for Todo AI Chatbot
Exposes task operations as tools for AI agents to use
"""

import asyncio
import logging
from typing import Dict, Any, List
from mcp.server import Server
from mcp.types import TextContent, ToolCallResult
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
import os
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize MCP server
server = Server("todo-mcp-server")

# Database setup - using the existing database connection
from app.database import get_engine
from app.models.task import Task
from sqlmodel import Session, select
from datetime import datetime

# Tool Definitions for MCP
@server.tool(
    "add_task",
    description="Add a new task for a user. Use when user wants to create a new task.",
    parameters={
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "The title of the task to add"},
            "description": {"type": "string", "description": "Description of the task"},
            "user_id": {"type": "string", "description": "ID of the user adding the task"}
        },
        "required": ["title", "user_id"]
    }
)
async def add_task(title: str, user_id: str, description: str = "") -> ToolCallResult:
    """
    Add a new task for a user.
    """
    logger.info(f"Adding task for user {user_id}: {title}")

    try:
        engine = get_engine()
        with Session(engine) as session:
            # Create the task object using the Task model with user_id
            new_task = Task(
                user_id=user_id,
                title=title,
                description=description or "",
                completed=False
            )

            session.add(new_task)
            session.commit()
            session.refresh(new_task)

            # Prepare result
            result = {
                "success": True,
                "task_id": new_task.id,
                "message": f"Task '{title}' has been added successfully with ID {new_task.id}"
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


@server.tool(
    "list_tasks",
    description="List all tasks for a user with optional filtering. Use when user wants to see their tasks.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ID of the user whose tasks to list"},
            "completed": {"type": "boolean", "description": "Filter by completion status (true=completed, false=not completed, null=all)"}
        },
        "required": ["user_id"]
    }
)
async def list_tasks(user_id: str, completed: bool = None) -> ToolCallResult:
    """
    List all tasks for a user with optional filtering.
    """
    logger.info(f"Listing tasks for user {user_id}, completed={completed}")

    try:
        engine = get_engine()
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


@server.tool(
    "update_task",
    description="Update an existing task for a user. Use when user wants to modify a task.",
    parameters={
        "type": "object",
        "properties": {
            "task_id": {"type": "integer", "description": "ID of the task to update"},
            "title": {"type": "string", "description": "New title for the task"},
            "description": {"type": "string", "description": "New description for the task"},
            "completed": {"type": "boolean", "description": "New completion status for the task"},
            "user_id": {"type": "string", "description": "ID of the user who owns the task"}
        },
        "required": ["task_id", "user_id"]
    }
)
async def update_task(
    task_id: int,
    user_id: str,
    title: str = None,
    description: str = None,
    completed: bool = None
) -> ToolCallResult:
    """
    Update an existing task for a user.
    """
    logger.info(f"Updating task {task_id} for user {user_id}")

    try:
        engine = get_engine()
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


@server.tool(
    "delete_task",
    description="Delete a task for a user. Use when user wants to remove a task.",
    parameters={
        "type": "object",
        "properties": {
            "task_id": {"type": "integer", "description": "ID of the task to delete"},
            "user_id": {"type": "string", "description": "ID of the user who owns the task"}
        },
        "required": ["task_id", "user_id"]
    }
)
async def delete_task(task_id: int, user_id: str) -> ToolCallResult:
    """
    Delete a task for a user.
    """
    logger.info(f"Deleting task {task_id} for user {user_id}")

    try:
        engine = get_engine()
        with Session(engine) as session:
            # Find the task by ID and user_id to ensure ownership
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
                "message": f"Task '{target_task.title}' (ID: {task_id}) deleted successfully"
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


@server.tool(
    "toggle_task_completion",
    description="Toggle the completion status of a task for a user. Use when user wants to mark a task as done or undone.",
    parameters={
        "type": "object",
        "properties": {
            "task_id": {"type": "integer", "description": "ID of the task to toggle"},
            "user_id": {"type": "string", "description": "ID of the user who owns the task"}
        },
        "required": ["task_id", "user_id"]
    }
)
async def toggle_task_completion(task_id: int, user_id: str) -> ToolCallResult:
    """
    Toggle the completion status of a task for a user.
    """
    logger.info(f"Toggling completion for task {task_id} for user {user_id}")

    try:
        engine = get_engine()
        with Session(engine) as session:
            # Find the task by ID and user_id to ensure ownership
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
                "message": f"Task '{target_task.title}' (ID: {task_id}) completion status toggled to {'completed' if target_task.completed else 'not completed'}"
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


async def main():
    """Run the MCP server."""
    # Check if running in MCP mode
    if "--mcp" in sys.argv or "MCP_MODE" in os.environ:
        logger.info("Starting MCP server...")
        async with server.run():
            logger.info("MCP server is running. Press Ctrl+C to stop.")
            try:
                # Keep the server running
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                logger.info("Shutting down MCP server...")
    else:
        # For testing purposes
        logger.info("MCP Server initialized. Run with --mcp flag to start the server.")


if __name__ == "__main__":
    asyncio.run(main())