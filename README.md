---
title: Todo AI Chatbot
emoji: 🤖
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
license: mit
---

# Todo AI Chatbot

An AI-powered Todo application with natural language processing capabilities.

## Features

- Natural language task management
- AI assistant for creating, updating, and managing tasks
- Real-time chat interface
- PostgreSQL database integration
- Conversational task management

## Usage

1. Type your task in natural language (e.g., "Add a task to buy groceries")
2. The AI assistant will create, update, or manage tasks based on your input
3. Ask questions like "Show my tasks" or "Mark task 1 as complete"

## Environment Variables

To run this application, you'll need the following environment variables:

- `DATABASE_URL`: PostgreSQL database URL
- `OPENAI_API_KEY`: OpenAI API key (optional, uses mock agent if not provided)
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-4-turbo-preview)

## API Endpoints

- `/chat` - Chat with the AI assistant
- `/chat/conversations` - List conversations
- `/api/{user_id}/tasks` - Task management API

## Built With

- FastAPI
- SQLModel
- OpenAI Assistant API
- React/Next.js (frontend)
- PostgreSQL

## License

MIT