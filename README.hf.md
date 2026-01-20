# AI-Powered Todo Chatbot

This is an AI-powered todo application that allows users to manage their tasks through natural language conversations. Built with FastAPI backend and integrated with OpenAI's ChatGPT, this application demonstrates the power of conversational AI for task management.

## Features

- 🤖 **Natural Language Processing**: Communicate with your todo list using everyday language
- ✅ **Task Management**: Create, update, complete, and delete tasks
- 💬 **Conversational Interface**: Talk to your todo list like a digital assistant
- 📱 **Responsive Design**: Works seamlessly across devices
- 🔐 **Secure Authentication**: User-specific task management

## How to Use

1. Start a conversation by typing a natural language command like:
   - "Add a task to buy groceries"
   - "Show me my incomplete tasks"
   - "Mark task 'buy groceries' as complete"
   - "Delete the meeting reminder task"

2. The AI assistant will interpret your commands and manage your todo list accordingly.

## Technical Details

- **Backend**: FastAPI with SQLModel and PostgreSQL
- **AI Integration**: OpenAI GPT models with MCP (Model Context Protocol) tools
- **Frontend**: Next.js with modern UI/UX
- **Database**: Neon Serverless PostgreSQL for persistent storage

## Architecture

This application uses an advanced architecture combining:
- FastAPI backend with RESTful API endpoints
- OpenAI Agents SDK for intelligent task management
- MCP (Model Context Protocol) for secure tool integration
- SQLModel for type-safe database operations

## Environment Variables Required

- `OPENAI_API_KEY`: Your OpenAI API key for AI functionality
- `NEON_DB_URL`: Database URL for persistent storage (optional, uses SQLite as fallback)

---
Built with ❤️ using Claude Code and Spec-Driven Development methodology.