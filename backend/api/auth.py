"""Authentication endpoints for the frontend."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user_id: str
    email: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str


@router.post("/login")
async def login(request: LoginRequest):
    """Login endpoint that returns a token and user info."""
    # For demo purposes, we'll create a simple user
    # In a real app, you'd validate credentials against a database
    user_id = f"user_{request.email.split('@')[0]}"

    return {
        "token": f"demo_token_{request.email}",
        "user_id": user_id,
        "email": request.email
    }


@router.post("/register")
async def register(request: RegisterRequest):
    """Register endpoint that creates a new user."""
    # For demo purposes, we'll create a simple user
    # In a real app, you'd create a user in the database
    user_id = f"user_{request.email.split('@')[0]}"

    return {
        "token": f"demo_token_{request.email}",
        "user_id": user_id,
        "email": request.email
    }


@router.get("/me")
async def get_user():
    """Get current user info."""
    # For demo purposes, return a placeholder user
    # In a real app, you'd extract user info from the token
    return {
        "user_id": "user_demo",
        "email": "demo@example.com",
        "name": "Demo User"
    }