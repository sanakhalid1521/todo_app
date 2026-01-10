"""
MCP Tools Definition for Todo AI Chatbot
Defines the tools that will be available to AI agents
"""

from typing import List
from pydantic import BaseModel, Field


# Define OpenAI-compatible tools
MCP_TOOLS: List[dict] = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task for a user. Use when user wants to create a new task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The title of the task to add"},
                    "description": {"type": "string", "description": "Description of the task"},
                    "user_id": {"type": "string", "description": "ID of the user adding the task"}
                },
                "required": ["title", "user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks for a user with optional filtering. Use when user wants to see their tasks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "ID of the user whose tasks to list"},
                    "completed": {"type": "boolean", "description": "Filter by completion status (true=completed, false=not completed, null=all)"}
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update an existing task for a user. Use when user wants to modify a task.",
            "parameters": {
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
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task for a user. Use when user wants to remove a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "ID of the task to delete"},
                    "user_id": {"type": "string", "description": "ID of the user who owns the task"}
                },
                "required": ["task_id", "user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "toggle_task_completion",
            "description": "Toggle the completion status of a task for a user. Use when user wants to mark a task as done or undone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "ID of the task to toggle"},
                    "user_id": {"type": "string", "description": "ID of the user who owns the task"}
                },
                "required": ["task_id", "user_id"]
            }
        }
    }
]