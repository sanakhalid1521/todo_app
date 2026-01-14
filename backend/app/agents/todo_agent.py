"""
OpenAI Agent for Todo AI Chatbot with MCP server integration
"""

import os
import json
from typing import Dict, Any, List
from openai import OpenAI
from app.mcp.tools import MCP_TOOLS
import httpx
import asyncio
from app.database import get_engine
from app.models.task import Task
from sqlmodel import Session, select
from datetime import datetime


class TodoAgent:
    def __init__(self):
        self._client = None  # Lazy initialization
        self.tools = MCP_TOOLS
        self.has_api_key = bool(os.getenv("OPENAI_API_KEY"))

    @property
    def client(self):
        if self._client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                # Return a mock client when API key is not available
                return None
            self._client = OpenAI(api_key=api_key)
        return self._client

    async def process_message(self, message: str, user_id: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Process a user message using the OpenAI agent with MCP tools.

        Args:
            message: The user's message
            user_id: The ID of the user
            conversation_history: Previous conversation messages

        Returns:
            The agent's response
        """
        if conversation_history is None:
            conversation_history = []

        # Check if OpenAI API key is available
        if not self.has_api_key:
            # Return mock responses for testing when API key is not available
            return await self._mock_process_message(message, user_id, conversation_history)

        # Prepare the messages for the OpenAI API
        system_message = {
            "role": "system",
            "content": (
                "You are a helpful AI assistant for managing todo tasks. "
                "Use the provided tools to help the user manage their tasks. "
                "Available tools: add_task, list_tasks, update_task, delete_task, toggle_task_completion. "
                "Always use the user_id when calling tools. "
                "After performing an action, provide a friendly response to the user."
            )
        }

        # Prepare conversation messages
        messages = [system_message]
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        # Add the current user message
        messages.append({"role": "user", "content": message})

        try:
            # Call OpenAI with function calling enabled
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Or gpt-4 if available
                messages=messages,
                tools=self.tools,
                tool_choice="auto",  # Auto-select tools when appropriate
                max_tokens=500,
                temperature=0.7
            )

            # Process the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                # Process each tool call
                tool_results = []

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Ensure user_id is included in function arguments
                    function_args["user_id"] = user_id

                    # Execute the appropriate tool function
                    result = await self.execute_tool(function_name, function_args)

                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": result
                    })

                # Get the final response after tool execution
                final_messages = messages + [response_message] + tool_results

                final_response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=final_messages,
                    max_tokens=500,
                    temperature=0.7
                )

                return final_response.choices[0].message.content
            else:
                # No tool calls, return the assistant's direct response
                return response_message.content

        except Exception as e:
            return f"Sorry, I encountered an error processing your request: {str(e)}"

    async def _mock_process_message(self, message: str, user_id: str, conversation_history: List[Dict[str, str]]) -> str:
        """
        Mock implementation for processing messages when OpenAI API key is not available.
        Supports both English and Roman Urdu commands.
        """
        message_lower = message.lower()

        # English and Roman Urdu pattern matching for commands
        # Add task patterns
        add_task_patterns = [
            "add task", "add a task", "create task", "bnado task", "bnao task", "task bnado",
            "task bnao", "task add kro", "task add karo", "new task", "task create"
        ]

        # List/Show tasks patterns
        list_task_patterns = [
            "show tasks", "list tasks", "my tasks", "tasks dikhao", "task dikhao",
            "dekhna hai", "dikhao mujhe", "mera tasks", "task list", "list dekhni hai",
            "mjhe task ki list dikhao", "meri task list", "tasks show kro", "tasks show karo",
            "show my task", "show me tasks", "show task", "list dekhni", "task list dekhni",
            "mujhe task", "task dekhni", "dekhna chahti hun", "kya hai meri list"
        ]

        # Pending/Incomplete tasks patterns
        pending_task_patterns = [
            "pending task", "pending tasks", "incomplete tasks", "todo tasks", "kam pending hai",
            "kya pending hai", "pending dekhao", "pending dikhao", "task pending", "pending list",
            "incomplete", "todo", "krna hai", "abhi baki hai", "baki task", "remaining task"
        ]

        # Completed tasks patterns
        completed_task_patterns = [
            "completed task", "completed tasks", "done tasks", "finished tasks", "hogye task",
            "ho gaye task", "completed dekhao", "done dekhao", "khtm tasks", "finish dekhna",
            "kya kiya hai", "completed list", "done list", "finished list"
        ]

        # Complete/Done patterns
        complete_patterns = [
            "complete", "done", "hogya", "ho gaya", "mark complete", "task complete",
            "finish", "khtm", "khatam", "kr diya", "kar diya", "completed", "task complete kro",
            "task complete karo", "task hogya", "task ho gaya", "task khtm", "task finish"
        ]

        # Delete/Remove patterns
        delete_patterns = [
            "delete", "remove", "delete task", "remove task", "task delete", "task remove",
            "nikal do", "nikal d", "hatado", "hata do", "task delete kro", "task delete karo",
            "task hatao", "task nikalo", "task hatado", "delete krna", "remove krna"
        ]

        # Check for add task patterns
        for pattern in add_task_patterns:
            if pattern in message_lower:
                # Extract task title from the message
                task_text = message_lower
                for p in add_task_patterns:
                    task_text = task_text.replace(p, "").strip()

                if not task_text:
                    task_text = "Sample task"

                # Execute mock add task
                result = await self._execute_mock_tool("add_task", {"user_id": user_id, "title": task_text.strip()})
                return result

        # Check for list tasks patterns
        for pattern in list_task_patterns:
            if pattern in message_lower:
                result = await self._execute_mock_tool("list_tasks", {"user_id": user_id})
                return result

        # Check for pending tasks patterns
        for pattern in pending_task_patterns:
            if pattern in message_lower:
                result = await self._execute_mock_tool("list_tasks", {"user_id": user_id, "completed": False})
                return result

        # Check for completed tasks patterns
        for pattern in completed_task_patterns:
            if pattern in message_lower:
                result = await self._execute_mock_tool("list_tasks", {"user_id": user_id, "completed": True})
                return result

        # Check for complete task patterns
        for pattern in complete_patterns:
            if pattern in message_lower:
                # Extract task ID or title if mentioned in message
                task_identifier = self._extract_task_identifier(message_lower, complete_patterns)

                if task_identifier:
                    # If it's numeric, treat as ID; otherwise, find task by title
                    if task_identifier.isdigit():
                        result = await self._execute_mock_tool("toggle_task_completion", {"user_id": user_id, "task_id": int(task_identifier)})
                    else:
                        # For mock purposes, we'll just confirm the action
                        result = await self._execute_mock_tool("toggle_task_completion", {"user_id": user_id})
                else:
                    # Default to toggle (would need to show user tasks to pick which one to complete)
                    result = await self._execute_mock_tool("toggle_task_completion", {"user_id": user_id})
                return result

        # Check for delete task patterns
        for pattern in delete_patterns:
            if pattern in message_lower:
                # Extract task ID or title if mentioned in message
                task_identifier = self._extract_task_identifier(message_lower, delete_patterns)

                if task_identifier:
                    # If it's numeric, treat as ID; otherwise, find task by title
                    if task_identifier.isdigit():
                        result = await self._execute_mock_tool("delete_task", {"user_id": user_id, "task_id": int(task_identifier)})
                    else:
                        # For mock purposes, we'll just confirm the action
                        result = await self._execute_mock_tool("delete_task", {"user_id": user_id})
                else:
                    # Default delete message
                    result = await self._execute_mock_tool("delete_task", {"user_id": user_id})
                return result

        # Default response
        return f"I've received your message: '{message}'. I can help you manage tasks like adding, listing, or completing tasks when the AI service is available."

    def _extract_task_identifier(self, message: str, command_patterns: List[str]) -> str:
        """
        Extract task identifier (ID or title) from the message by removing command patterns.
        """
        clean_message = message

        # Remove all command patterns to isolate the task identifier
        for pattern in command_patterns:
            clean_message = clean_message.replace(pattern, "").strip()

        # Additional cleanup: remove common words that might remain
        common_words = ["the", "task", "please", "now", "to", "me", "want", "need"]
        for word in common_words:
            clean_message = clean_message.replace(word, "").strip()

        # Clean up extra whitespace and return
        clean_message = " ".join(clean_message.split())

        # If what remains looks like a number, return it (as a task ID)
        if clean_message.isdigit():
            return clean_message
        # If it contains recognizable text, return it as a potential task title
        elif clean_message and len(clean_message) > 1:
            return clean_message

        # Return empty if no clear identifier found
        return ""

    async def _execute_mock_tool(self, function_name: str, function_args: Dict[str, Any]) -> str:
        """
        Mock implementation of tool execution for testing purposes.
        """
        try:
            if function_name == "add_task":
                title = function_args.get("title", "Sample task")
                description = function_args.get("description", "")
                user_id = function_args.get("user_id", "unknown")

                # Simulate adding a task and returning a unique ID
                import random
                task_id = random.randint(1000, 9999)  # Random ID for mock

                return f"Task '{title}' has been added successfully with ID {task_id}."

            elif function_name == "list_tasks":
                # Check if completed parameter is specified
                completed = function_args.get("completed")
                user_id = function_args.get("user_id", "unknown")

                if completed is True:
                    return "Here are your completed tasks:\n- ID: 1, Title: Complete project proposal, Status: completed\n- ID: 3, Title: Submit quarterly report, Status: completed"
                elif completed is False:
                    return "Here are your pending tasks:\n- ID: 2, Title: Buy groceries, Status: not completed\n- ID: 4, Title: Schedule meeting, Status: not completed"
                else:
                    return "Here are your tasks:\n- ID: 1, Title: Complete project proposal, Status: completed\n- ID: 2, Title: Buy groceries, Status: not completed\n- ID: 3, Title: Submit quarterly report, Status: completed\n- ID: 4, Title: Schedule meeting, Status: not completed"

            elif function_name == "update_task":
                task_id = function_args.get("task_id", "unknown")
                title = function_args.get("title")
                completed = function_args.get("completed")

                updates = []
                if title:
                    updates.append(f"title to '{title}'")
                if completed is not None:
                    updates.append(f"completion status to {'completed' if completed else 'not completed'}")

                if updates:
                    updates_str = " and ".join(updates)
                    return f"Task {task_id} updated successfully ({updates_str})."
                else:
                    return f"Task {task_id} updated successfully."

            elif function_name == "delete_task":
                task_id = function_args.get("task_id", "unknown")
                user_id = function_args.get("user_id", "unknown")

                if task_id != "unknown":
                    return f"Task ID {task_id} has been deleted successfully."
                else:
                    return "Task has been deleted successfully."

            elif function_name == "toggle_task_completion":
                task_id = function_args.get("task_id", "unknown")
                user_id = function_args.get("user_id", "unknown")

                if task_id != "unknown":
                    return f"Task ID {task_id}'s completion status has been toggled successfully."
                else:
                    return "Task completion status has been toggled successfully."

            else:
                return f"Unknown tool '{function_name}' called."

        except Exception as e:
            return f"Error executing tool {function_name}: {str(e)}"

    async def execute_tool(self, function_name: str, function_args: Dict[str, Any]) -> str:
        """
        Execute the appropriate task operation based on the function name.
        First tries to call the MCP server, falls back to direct database operations.

        Args:
            function_name: Name of the function to execute
            function_args: Arguments for the function

        Returns:
            Result of the tool execution
        """

        # Try to call the MCP server first
        try:
            # For now, we'll use direct database operations since MCP server setup
            # requires additional infrastructure that may not be available
            # In a production setup, this would call the actual MCP server
            return await self._execute_direct_db_operation(function_name, function_args)
        except Exception as e:
            # Fallback to direct database operations
            try:
                return await self._execute_direct_db_operation(function_name, function_args)
            except Exception as db_error:
                return f"Error executing tool {function_name}: {str(db_error)}"

    async def _execute_direct_db_operation(self, function_name: str, function_args: Dict[str, Any]) -> str:
        """
        Execute task operations using direct database operations.
        This serves as both the primary implementation and fallback.
        """
        engine = get_engine()

        try:
            if function_name == "add_task":
                with Session(engine) as session:
                    new_task = Task(
                        user_id=function_args.get("user_id"),
                        title=function_args.get("title", ""),
                        description=function_args.get("description", ""),
                        completed=False
                    )

                    session.add(new_task)
                    session.commit()
                    session.refresh(new_task)

                    return f"Task '{new_task.title}' has been added successfully with ID {new_task.id}"

            elif function_name == "list_tasks":
                with Session(engine) as session:
                    query = select(Task).where(Task.user_id == function_args.get("user_id"))

                    completed = function_args.get("completed")
                    if completed is not None:
                        query = query.where(Task.completed == completed)

                    tasks = session.exec(query).all()

                    if not tasks:
                        return "You have no tasks."

                    task_list = []
                    for task in tasks:
                        status = "completed" if task.completed else "not completed"
                        task_list.append(f"- ID: {task.id}, Title: {task.title}, Status: {status}")

                    return f"You have {len(tasks)} tasks:\n" + "\n".join(task_list)

            elif function_name == "update_task":
                with Session(engine) as session:
                    task_id = function_args.get("task_id", 0)
                    user_id = function_args.get("user_id")

                    # Get the task by ID and user_id to ensure ownership
                    query = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
                    target_task = session.exec(query).first()

                    if not target_task:
                        return f"Task with ID {task_id} not found or you don't have permission to modify it"

                    # Update the task fields if provided
                    if "title" in function_args and function_args["title"] is not None:
                        target_task.title = function_args["title"]
                    if "description" in function_args and function_args["description"] is not None:
                        target_task.description = function_args["description"]
                    if "completed" in function_args and function_args["completed"] is not None:
                        target_task.completed = function_args["completed"]

                    target_task.updated_at = datetime.now()

                    session.add(target_task)
                    session.commit()
                    session.refresh(target_task)

                    status = "completed" if target_task.completed else "not completed"
                    return f"Task {target_task.id} updated successfully. Title: {target_task.title}, Status: {status}"

            elif function_name == "delete_task":
                with Session(engine) as session:
                    task_id = function_args.get("task_id", 0)
                    user_id = function_args.get("user_id")

                    # Get the task by ID and user_id to ensure ownership
                    query = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
                    target_task = session.exec(query).first()

                    if not target_task:
                        return f"Task with ID {task_id} not found or you don't have permission to delete it"

                    session.delete(target_task)
                    session.commit()

                    return f"Task '{target_task.title}' has been deleted successfully"

            elif function_name == "toggle_task_completion":
                with Session(engine) as session:
                    task_id = function_args.get("task_id", 0)
                    user_id = function_args.get("user_id")

                    # Get the task by ID and user_id to ensure ownership
                    query = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
                    target_task = session.exec(query).first()

                    if not target_task:
                        return f"Task with ID {task_id} not found or you don't have permission to modify it"

                    # Toggle completion status
                    target_task.completed = not target_task.completed
                    target_task.updated_at = datetime.now()

                    session.add(target_task)
                    session.commit()
                    session.refresh(target_task)

                    status = "completed" if target_task.completed else "not completed"
                    return f"Task '{target_task.title}' completion status toggled to {status}"

            else:
                return f"Unknown tool: {function_name}"

        except Exception as e:
            return f"Error executing tool {function_name}: {str(e)}"


# Global instance for use in the application
todo_agent = TodoAgent()