"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from api.todos import router as todos_router
from app.routers.tasks import router as tasks_router
from api.auth import router as auth_router
from app.database import init_db

# Conditionally import chat router to avoid dependency issues
try:
    from app.routers.chat import router as chat_router
    CHAT_AVAILABLE = True
except ImportError as e:
    print(f"Chat router not available: {e}")
    CHAT_AVAILABLE = False

app = FastAPI(
    title="Todo AI Chatbot",
    description="AI-powered Todo Application with Chat Interface",
    version="1.0.0",
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001", "http://localhost:8000", "*"],  # Allow frontend and backend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    print("Starting up application...")
    await init_db()
    print("Application started successfully!")


app.include_router(todos_router)
app.include_router(tasks_router)
app.include_router(auth_router)
if CHAT_AVAILABLE:
    app.include_router(chat_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to Todo API", "docs": "/docs"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
