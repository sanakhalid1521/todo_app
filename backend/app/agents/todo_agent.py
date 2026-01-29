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
from database import get_async_session
from app.models.task import Task
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
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
        This version connects to the database for actual operations.
        """
        message_lower = message.lower()

        # English and Roman Urdu pattern matching for commands based on agent behavior specification
        # Task Creation - When user mentions adding/creating/remembering something
        add_task_patterns = [
            "add ", "create ", "make ", "remember ", "bnado ", "bnao ", "task bnado",
            "task bnao", "task add kro", "task add karo", "new ", "create a", "add a"
        ]

        # Task Listing - When user asks to see/show/list tasks
        list_task_patterns = [
            "show ", "list ", "my ", "tasks ", "dikhao ", "dekhna ", "dekho ",
            "mere ", "mera ", "mujhe ", "list dekhni ", "show my", "show me",
            "what", "have", "got", "todo", "pending", "all"
        ]

        # Task Completion - When user says done/complete/finished
        complete_task_patterns = [
            "done", "complete", "finished", "hogya", "ho gaya", "mark done", "mark complete",
            "finish", "khtm", "khatam", "kr diya", "kar diya", "completed", "task complete kro",
            "task complete karo", "task hogya", "task ho gaya", "task khtm", "task finish",
            "complete task", "finish task", "done task"
        ]

        # Task Deletion - When user says delete/remove/cancel
        delete_task_patterns = [
            "delete", "remove", "cancel", "delete task", "remove task", "task delete", "task remove",
            "nikal do", "nikal d", "hatado", "hata do", "task delete kro", "task delete karo",
            "task hatao", "task nikalo", "task hatado", "delete krna", "remove krna", "cancel task"
        ]

        # Task Update - When user says change/update/rename
        update_task_patterns = [
            "change", "update", "modify", "rename", "edit", "change task", "update task", "modify task",
            "rename task", "edit task", "update kro", "update karo", "badlo", "badliye", "thori"
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

                # Extract description if present (look for "and" or "description is")
                description = ""
                if " and description is " in message_lower:
                    desc_part = message_lower.split(" and description is ")[1]
                    description = desc_part.strip()

                # Execute actual database add task (not mock)
                function_args = {
                    "user_id": user_id,
                    "title": task_text.strip(),
                    "description": description
                }
                result = await self._execute_direct_db_operation("add_task", function_args)
                return result

        # Check for update task patterns
        for pattern in update_task_patterns:
            if pattern in message_lower:
                # Extract task ID or title if mentioned in message
                task_identifier = self._extract_task_identifier(message_lower, update_task_patterns)

                # Extract new title if available
                new_title = self._extract_new_title_from_message(message_lower, update_task_patterns)

                if task_identifier and task_identifier.isdigit():
                    function_args = {
                        "user_id": user_id,
                        "task_id": int(task_identifier),
                        "title": new_title or "Updated task"
                    }
                    result = await self._execute_direct_db_operation("update_task", function_args)
                else:
                    # For default update, we need a valid task ID - let's list tasks first to show available ones
                    result = "Please specify which task ID to update. Available tasks: " + await self._execute_direct_db_operation("list_tasks", {"user_id": user_id, "status": "all"})
                return result

        # Check for complete task patterns
        for pattern in complete_task_patterns:
            if pattern in message_lower:
                # Extract task ID or title if mentioned in message
                task_identifier = self._extract_task_identifier(message_lower, complete_task_patterns)

                if task_identifier and task_identifier.isdigit():
                    function_args = {
                        "user_id": user_id,
                        "task_id": int(task_identifier)
                    }
                    result = await self._execute_direct_db_operation("complete_task", function_args)
                else:
                    # For default completion, we need a valid task ID - list tasks first
                    result = "Please specify which task ID to complete. Available tasks: " + await self._execute_direct_db_operation("list_tasks", {"user_id": user_id, "status": "all"})
                return result

        # Check for delete task patterns
        for pattern in delete_task_patterns:
            if pattern in message_lower:
                # Extract task ID or title if mentioned in message
                task_identifier = self._extract_task_identifier(message_lower, delete_task_patterns)

                if task_identifier and task_identifier.isdigit():
                    function_args = {
                        "user_id": user_id,
                        "task_id": int(task_identifier)
                    }
                    result = await self._execute_direct_db_operation("delete_task", function_args)
                else:
                    # For default deletion, we need a valid task ID - list tasks first
                    result = "Please specify which task ID to delete. Available tasks: " + await self._execute_direct_db_operation("list_tasks", {"user_id": user_id, "status": "all"})
                return result

        # Check for list tasks patterns - check this last as it's more general
        for pattern in list_task_patterns:
            if pattern in message_lower:
                # Check for specific filters in the message
                if any(word in message_lower for word in ["pending", "incomplete", "todo", "krna hai", "baki"]):
                    result = await self._execute_direct_db_operation("list_tasks", {"user_id": user_id, "status": "pending"})
                elif any(word in message_lower for word in ["completed", "done", "finished", "hogye", "ho gaye"]):
                    result = await self._execute_direct_db_operation("list_tasks", {"user_id": user_id, "status": "completed"})
                else:
                    result = await self._execute_direct_db_operation("list_tasks", {"user_id": user_id, "status": "all"})
                return result

        # Default response
        return f"I've received your message: '{message}'. I can help you manage tasks like adding, listing, or completing tasks."

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

    def _extract_new_title_from_message(self, message: str, command_patterns: List[str]) -> str:
        """
        Extract new title from update commands in the message.
        """
        clean_message = message

        # Remove command patterns
        for pattern in command_patterns:
            clean_message = clean_message.replace(pattern, "").strip()

        # Look for keywords indicating a new title (like "to", "as", etc.)
        separators = [" to ", " as ", " with ", " - ", ": "]
        for sep in separators:
            parts = clean_message.split(sep)
            if len(parts) > 1:
                # Return the part after the separator (the new title)
                new_title = parts[1].strip()
                # Clean up any remaining common words
                common_words = ["the", "task", "please", "now", "to", "me", "want", "need"]
                for word in common_words:
                    new_title = new_title.replace(word, "").strip()
                new_title = " ".join(new_title.split())  # Clean up extra spaces
                if len(new_title) > 1:
                    return new_title

        # If no separator found, return what's left as potential new title
        for word in ["the", "task", "please", "now", "to", "me", "want", "need"]:
            clean_message = clean_message.replace(word, "").strip()
        clean_message = " ".join(clean_message.split())

        if len(clean_message) > 1:
            return clean_message

        return ""

    async def _execute_mock_tool(self, function_name: str, function_args: Dict[str, Any]) -> str:
        """
        Legacy mock implementation - this is no longer used since we now call actual database operations.
        Kept for compatibility but shouldn't be called in the updated flow.
        """
        print(f"WARNING: _execute_mock_tool called with {function_name}, this shouldn't happen in the new implementation!")
        return f"Mock operation for {function_name} - this function should not be called anymore."

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
        # Get async session
        async for session in get_async_session():
            try:
                if function_name == "add_task":
                    user_id = function_args.get("user_id")
                    title = function_args.get("title", "")
                    description = function_args.get("description", "")

                    # Debug: Print the values being used
                    print(f"DEBUG: Adding task for user_id: {user_id}, title: {title}")

                    new_task = Task(
                        user_id=user_id,
                        title=title,
                        description=description,
                        completed=False
                    )

                    session.add(new_task)
                    await session.commit()
                    await session.refresh(new_task)

                    # Debug: Confirm the task was created
                    print(f"DEBUG: Created task with ID {new_task.id} for user {new_task.user_id}")

                    return f'{{"task_id": {new_task.id}, "status": "created", "title": "{new_task.title}"}}'

                elif function_name == "list_tasks":
                    # Get user_id from function_args
                    user_id = function_args.get("user_id")

                    # Debug: Print the user_id being used for the query
                    print(f"DEBUG: Querying tasks for user_id: {user_id}")

                    query = select(Task).where(Task.user_id == user_id)

                    # Handle status filtering according to spec
                    status_filter = function_args.get("status", "all")
                    if status_filter == "completed":
                        query = query.where(Task.completed == True)
                    elif status_filter == "pending":
                        query = query.where(Task.completed == False)

                    result = await session.execute(query)
                    tasks = result.scalars().all()

                    # Debug: Print number of tasks found
                    print(f"DEBUG: Found {len(tasks)} tasks for user {user_id}")

                    # Format response according to specification
                    task_list = []
                    for task in tasks:
                        task_dict = {
                            "id": task.id,
                            "title": task.title,
                            "completed": task.completed
                        }
                        task_list.append(task_dict)

                    import json
                    return json.dumps(task_list)

                elif function_name == "update_task":
                    task_id = function_args.get("task_id", 0)
                    user_id = function_args.get("user_id")

                    print(f"DEBUG: Attempting to update task_id {task_id} for user {user_id}")

                    # Get the task by ID and user_id to ensure ownership
                    query = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
                    result = await session.execute(query)
                    target_task = result.scalar_one_or_none()

                    if not target_task:
                        return f"Task with ID {task_id} not found or you don't have permission to modify it"

                    print(f"DEBUG: Found task {target_task.id} titled '{target_task.title}' to update")

                    # Update the task fields if provided
                    if "title" in function_args and function_args["title"] is not None:
                        target_task.title = function_args["title"]
                        print(f"DEBUG: Updated title to '{target_task.title}'")
                    if "description" in function_args and function_args["description"] is not None:
                        target_task.description = function_args["description"]
                        print(f"DEBUG: Updated description to '{target_task.description}'")

                    target_task.updated_at = datetime.now()

                    session.add(target_task)
                    await session.commit()
                    await session.refresh(target_task)

                    import json
                    return json.dumps({"task_id": target_task.id, "status": "updated", "title": target_task.title})

                elif function_name == "delete_task":
                    task_id = function_args.get("task_id", 0)
                    user_id = function_args.get("user_id")

                    print(f"DEBUG: Attempting to delete task_id {task_id} for user {user_id}")

                    # Get the task by ID and user_id to ensure ownership
                    query = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
                    result = await session.execute(query)
                    target_task = result.scalar_one_or_none()

                    if not target_task:
                        return f"Task with ID {task_id} not found or you don't have permission to delete it"

                    print(f"DEBUG: Found task {target_task.id} titled '{target_task.title}' to delete")

                    # Store the title before deletion to include in the response
                    title_before_deletion = target_task.title

                    await session.delete(target_task)
                    await session.commit()

                    import json
                    return json.dumps({"task_id": target_task.id, "status": "deleted", "title": title_before_deletion})

                elif function_name == "complete_task":
                    task_id = function_args.get("task_id", 0)
                    user_id = function_args.get("user_id")

                    print(f"DEBUG: Attempting to complete task_id {task_id} for user {user_id}")

                    # Get the task by ID and user_id to ensure ownership
                    query = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
                    result = await session.execute(query)
                    target_task = result.scalar_one_or_none()

                    if not target_task:
                        return f"Task with ID {task_id} not found or you don't have permission to modify it"

                    print(f"DEBUG: Found task {target_task.id} titled '{target_task.title}' to complete")

                    # Mark as completed
                    target_task.completed = True
                    target_task.updated_at = datetime.now()

                    session.add(target_task)
                    await session.commit()
                    await session.refresh(target_task)

                    import json
                    return json.dumps({"task_id": target_task.id, "status": "completed", "title": target_task.title})

                else:
                    return f"Unknown tool: {function_name}"

            except Exception as e:
                return f"Error executing tool {function_name}: {str(e)}"


# Global instance for use in the application
todo_agent = TodoAgent()