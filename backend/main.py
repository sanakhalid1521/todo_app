"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.todos import router as todos_router
from api.tasks import router as tasks_router
from api.auth import router as auth_router
from database import init_db

app = FastAPI(
    title="Todo API",
    description="A simple Todo API with FastAPI and PostgreSQL",
    version="1.0.0",
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    await init_db()


app.include_router(todos_router)
app.include_router(tasks_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to Todo API", "docs": "/docs"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
