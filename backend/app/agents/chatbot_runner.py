#!/usr/bin/env python3
"""
Chatbot runner script for the Todo AI Chatbot
"""

import asyncio
import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the agent and database modules using relative imports
from app.agents.todo_agent import TodoAgent
from database import init_db

# Create global agent instance
agent = TodoAgent()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Initializing database...")
    await init_db()
    print("Database initialized. Chatbot service starting...")

    yield

    # Shutdown
    print("Shutting down chatbot service...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Todo AI Chatbot Service is running!"}

@app.post("/chat")
async def chat(message: str, user_id: str = "default_user"):
    """Process a chat message using the Todo AI agent."""
    try:
        response = await agent.process_message(message, user_id)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "has_openai": agent.has_api_key}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)