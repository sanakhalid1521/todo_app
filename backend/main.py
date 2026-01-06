"""Main FastAPI application."""
from fastapi import FastAPI

from api.todos import router as todos_router
from database import init_db

app = FastAPI(
    title="Todo API",
    description="A simple Todo API with FastAPI and PostgreSQL",
    version="1.0.0",
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    await init_db()


app.include_router(todos_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to Todo API", "docs": "/docs"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
