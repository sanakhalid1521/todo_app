# Phase II - Full Stack Web Application Specification

## Overview
This phase implements the full-stack web application with Next.js frontend and FastAPI backend, incorporating all required todo features.

## Requirements
- Next.js frontend with App Router
- FastAPI backend with SQLModel and Neon DB
- Complete CRUD functionality for todo items
- Authentication system
- Responsive UI design

## Todo Features Implementation
1. Add Task – Create new todo items ✓
2. Delete Task – Remove tasks from the list ✓
3. Update Task – Modify existing task details ✓
4. View Task List – Display all tasks ✓
5. Mark as Complete – Toggle task completion status ✓
6. Priorities & Tags/Categories – Assign levels and labels ✓
7. Search & Filter – Search by keyword; filter by status ✓
8. Sort Tasks – Reorder by due date, priority, or alphabetically ✓
9. Due Dates & Time Reminders – Set deadlines with date/time pickers ✓

## Tech Stack
- Frontend: Next.js 14+ (App Router)
- Backend: FastAPI with SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Custom implementation
- Styling: Tailwind CSS with glass morphism effects

## API Endpoints
- GET /api/{user_id}/tasks - List all tasks for user
- POST /api/{user_id}/tasks - Create new task
- GET /api/{user_id}/tasks/{task_id} - Get specific task
- PUT /api/{user_id}/tasks/{task_id} - Update task
- DELETE /api/{user_id}/tasks/{task_id} - Delete task
- PATCH /api/{user_id}/tasks/{task_id}/toggle - Toggle completion

## Frontend Structure
- App Router with (auth) route groups
- Context providers for modal, search, and auth
- Component-based UI with glass morphism design
- Client-side data fetching and state management

## Database Models
- Todo model with title, description, completion status
- User model for authentication
- Relationship between users and todos