"""Task router with CRUD operations."""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.security import extract_user_id_from_token
from app.database import get_engine
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

# Import SSE broadcasting function
try:
    from app.routers.sse import broadcast_task_event
    SSE_AVAILABLE = True
except ImportError as e:
    print(f"SSE import error: {e}")
    SSE_AVAILABLE = False

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

    # Special case: if using demo user, ensure the user exists in the database
    if user_id == 'user-demo':
        # Check if demo user exists, create if not
        from app.models.user import User
        demo_user = db.query(User).filter(User.id == user_id).first()
        if not demo_user:
            demo_user = User(
                id=user_id,
                email="demo@example.com",
                password_hash="",  # Empty hash for demo user
            )
            db.add(demo_user)
            db.commit()

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

    # Special case: if using demo user, ensure the user exists in the database
    if user_id == 'user-demo':
        # Check if demo user exists, create if not
        from app.models.user import User
        demo_user = db.query(User).filter(User.id == user_id).first()
        if not demo_user:
            demo_user = User(
                id=user_id,
                email="demo@example.com",
                password_hash="",  # Empty hash for demo user
            )
            db.add(demo_user)
            db.commit()

    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        category=task_data.category if hasattr(task_data, 'category') else Task.category.field.default,
        priority=task_data.priority if hasattr(task_data, 'priority') else Task.priority.field.default,
        due_date=task_data.due_date if hasattr(task_data, 'due_date') else None
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    # Broadcast task creation event via SSE if available
    if SSE_AVAILABLE:
        try:
            broadcast_task_event("task_created", task, user_id)
        except Exception as e:
            print(f"Error broadcasting task creation event: {e}")

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

    # Special case: if using demo user, ensure the user exists in the database
    if user_id == 'user-demo':
        # Check if demo user exists, create if not
        from app.models.user import User
        demo_user = db.query(User).filter(User.id == user_id).first()
        if not demo_user:
            demo_user = User(
                id=user_id,
                email="demo@example.com",
                password_hash="",  # Empty hash for demo user
            )
            db.add(demo_user)
            db.commit()

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

    # Special case: if using demo user, ensure the user exists in the database
    if user_id == 'user-demo':
        # Check if demo user exists, create if not
        from app.models.user import User
        demo_user = db.query(User).filter(User.id == user_id).first()
        if not demo_user:
            demo_user = User(
                id=user_id,
                email="demo@example.com",
                password_hash="",  # Empty hash for demo user
            )
            db.add(demo_user)
            db.commit()

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

    # Broadcast task update event via SSE if available
    if SSE_AVAILABLE:
        try:
            broadcast_task_event("task_updated", task, user_id)
        except Exception as e:
            print(f"Error broadcasting task update event: {e}")

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

    # Special case: if using demo user, ensure the user exists in the database
    if user_id == 'user-demo':
        # Check if demo user exists, create if not
        from app.models.user import User
        demo_user = db.query(User).filter(User.id == user_id).first()
        if not demo_user:
            demo_user = User(
                id=user_id,
                email="demo@example.com",
                password_hash="",  # Empty hash for demo user
            )
            db.add(demo_user)
            db.commit()

    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Store task info for broadcasting before deletion
    task_info = {
        "id": task.id,
        "user_id": task.user_id,
        "title": task.title
    }

    db.delete(task)
    db.commit()

    # Broadcast task deletion event via SSE if available
    if SSE_AVAILABLE:
        try:
            # We can't pass the deleted task object, so we create a minimal one for the broadcast
            from datetime import datetime
            temp_task = Task(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                category=task.category,
                priority=task.priority,
                due_date=task.due_date,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            broadcast_task_event("task_deleted", temp_task, user_id)
        except Exception as e:
            print(f"Error broadcasting task deletion event: {e}")


@router.get("/{user_id}/tasks/search", response_model=list[TaskResponse])
async def search_tasks(
    user_id: str,
    q: str = None,
    status: str = None,
    category: str = None,
    priority: str = None,
    due_date: str = None,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Search tasks by title, description, or content with optional filters."""
    if not verify_user_authorization(authorization, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    # Special case: if using demo user, ensure the user exists in the database
    if user_id == 'user-demo':
        # Check if demo user exists, create if not
        from app.models.user import User
        demo_user = db.query(User).filter(User.id == user_id).first()
        if not demo_user:
            demo_user = User(
                id=user_id,
                email="demo@example.com",
                password_hash="",  # Empty hash for demo user
            )
            db.add(demo_user)
            db.commit()

    # Build query
    query = db.query(Task).filter(Task.user_id == user_id)

    # Apply search filter if query provided
    if q:
        search_term = f"%{q}%"
        query = query.filter(
            (Task.title.ilike(search_term)) |
            (Task.description.ilike(search_term))
        )

    # Apply status filter
    if status:
        if status.lower() == "completed":
            query = query.filter(Task.completed == True)
        elif status.lower() == "pending":
            query = query.filter(Task.completed == False)

    # Apply category filter
    if category:
        query = query.filter(Task.category == category)

    # Apply priority filter
    if priority:
        query = query.filter(Task.priority == priority)

    # Apply due date filter
    if due_date:
        from datetime import datetime
        if due_date.lower() == "overdue":
            now = datetime.utcnow()
            query = query.filter(Task.due_date < now).filter(Task.completed == False)
        elif due_date.lower() == "today":
            from datetime import datetime, timedelta
            today_start = datetime.combine(datetime.utcnow().date(), datetime.min.time())
            today_end = datetime.combine(datetime.utcnow().date(), datetime.max.time())
            query = query.filter(Task.due_date >= today_start).filter(Task.due_date <= today_end)
        elif due_date.lower() == "week":
            from datetime import datetime, timedelta
            week_start = datetime.utcnow() - timedelta(days=datetime.utcnow().weekday())
            week_end = week_start + timedelta(days=7)
            query = query.filter(Task.due_date >= week_start).filter(Task.due_date <= week_end)

    tasks = query.all()
    return tasks


@router.get("/{user_id}/tasks/stats")
async def get_task_stats(
    user_id: str,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Get task statistics for analytics dashboard."""
    if not verify_user_authorization(authorization, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    # Special case: if using demo user, ensure the user exists in the database
    if user_id == 'user-demo':
        # Check if demo user exists, create if not
        from app.models.user import User
        demo_user = db.query(User).filter(User.id == user_id).first()
        if not demo_user:
            demo_user = User(
                id=user_id,
                email="demo@example.com",
                password_hash="",  # Empty hash for demo user
            )
            db.add(demo_user)
            db.commit()

    # Get all tasks for the user
    all_tasks = db.query(Task).filter(Task.user_id == user_id).all()

    # Calculate statistics
    total = len(all_tasks)
    completed_count = sum(1 for task in all_tasks if task.completed)
    pending_count = total - completed_count
    completion_rate = (completed_count / total * 100) if total > 0 else 0

    # Count by category
    category_counts = {
        "work": 0,
        "personal": 0,
        "shopping": 0,
        "health": 0,
        "other": 0
    }
    for task in all_tasks:
        category_counts[task.category.value if hasattr(task.category, 'value') else task.category] += 1

    # Count by priority
    priority_counts = {
        "low": 0,
        "medium": 0,
        "high": 0,
        "urgent": 0
    }
    for task in all_tasks:
        priority_counts[task.priority.value if hasattr(task.priority, 'value') else task.priority] += 1

    # Count overdue, due today, due this week
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    overdue_count = sum(1 for task in all_tasks if task.due_date and task.due_date < now and not task.completed)

    today_start = datetime.combine(now.date(), datetime.min.time())
    today_end = datetime.combine(now.date(), datetime.max.time())
    due_today_count = sum(1 for task in all_tasks if
                          task.due_date and
                          today_start <= task.due_date <= today_end and
                          not task.completed)

    week_start = now - timedelta(days=now.weekday())
    week_end = week_start + timedelta(days=6)
    due_this_week_count = sum(1 for task in all_tasks if
                              task.due_date and
                              week_start <= task.due_date <= week_end and
                              not task.completed)

    # Prepare response
    stats = {
        "total": total,
        "completed": completed_count,
        "pending": pending_count,
        "completion_rate": round(completion_rate, 2),
        "by_category": category_counts,
        "by_priority": priority_counts,
        "overdue": overdue_count,
        "due_today": due_today_count,
        "due_this_week": due_this_week_count
    }

    return stats


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

    # Special case: if using demo user, ensure the user exists in the database
    if user_id == 'user-demo':
        # Check if demo user exists, create if not
        from app.models.user import User
        demo_user = db.query(User).filter(User.id == user_id).first()
        if not demo_user:
            demo_user = User(
                id=user_id,
                email="demo@example.com",
                password_hash="",  # Empty hash for demo user
            )
            db.add(demo_user)
            db.commit()

    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task.completed = not task.completed
    db.commit()
    db.refresh(task)

    # Broadcast task completion toggle event via SSE if available
    if SSE_AVAILABLE:
        try:
            broadcast_task_event("task_toggled", task, user_id)
        except Exception as e:
            print(f"Error broadcasting task toggle event: {e}")

    return task
