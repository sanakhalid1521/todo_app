"""Task router with CRUD operations."""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.security import extract_user_id_from_token
from app.database import get_engine
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/api", tags=["Tasks"])


def get_db():
    """Get database session."""
    engine = get_engine()
    with Session(engine) as session:
        yield session


def verify_user_authorization(authorization: str, user_id: str) -> bool:
    """Verify user is authorized to access this user's resources."""
    # Special case: allow access to 'user-demo' resources without strict token checking
    # This is for demo/testing purposes when no user is properly authenticated
    if user_id == 'user-demo':
        return True

    if not authorization or not authorization.startswith("Bearer "):
        return False

    token = authorization.replace("Bearer ", "")
    token_user_id = extract_user_id_from_token(token)

    return token_user_id == user_id


@router.get("/{user_id}/tasks", response_model=list[TaskResponse])
async def get_tasks(
    user_id: str,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Get all tasks for a user."""
    if not verify_user_authorization(authorization, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Create a new task for a user."""
    if not verify_user_authorization(authorization, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Get a single task."""
    if not verify_user_authorization(authorization, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Update a task."""
    if not verify_user_authorization(authorization, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update fields
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: int,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Delete a task."""
    if not verify_user_authorization(authorization, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()


@router.patch("/{user_id}/tasks/{task_id}/toggle", response_model=TaskResponse)
async def toggle_task(
    user_id: str,
    task_id: int,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Toggle task completion status."""
    if not verify_user_authorization(authorization, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task.completed = not task.completed
    db.commit()
    db.refresh(task)

    return task
