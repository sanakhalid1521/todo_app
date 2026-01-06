from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.todos import router as todos_router
from app.routers.tasks import router as tasks_router
from app.database import create_tables

app = FastAPI(
    title="Todo AI Chatbot",
    description="AI-powered Todo Application with Chat Interface",
    version="1.0.0",
)

# CORS middleware - allow all for Hugging Face deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Hugging Face
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    create_tables()

app.include_router(todos_router)
app.include_router(tasks_router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to Todo AI Chatbot API", "docs": "/docs"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# For Hugging Face Spaces
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)