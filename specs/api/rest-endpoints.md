# REST API Endpoints Specification

## Overview
This document specifies all REST API endpoints for the Todo application.

## Base URL
`/api/{user_id}/tasks`

## Authentication
All endpoints require authentication and validate that the requesting user matches the user_id in the URL.

## Endpoints

### Task Management

#### GET /api/{user_id}/tasks
- Description: Retrieve all tasks for a specific user
- Query Parameters:
  - completed (optional): Filter by completion status (true/false)
- Response: Array of Task objects
- Status Codes:
  - 200: Success

#### POST /api/{user_id}/tasks
- Description: Create a new task for a user
- Request Body: TaskCreate object
- Response: Created Task object
- Status Codes:
  - 201: Created
  - 400: Invalid request data

#### GET /api/{user_id}/tasks/{task_id}
- Description: Retrieve a specific task
- Response: Task object
- Status Codes:
  - 200: Success
  - 404: Task not found

#### PUT /api/{user_id}/tasks/{task_id}
- Description: Update a specific task
- Request Body: TaskUpdate object
- Response: Updated Task object
- Status Codes:
  - 200: Success
  - 404: Task not found

#### DELETE /api/{user_id}/tasks/{task_id}
- Description: Delete a specific task
- Response: Success confirmation
- Status Codes:
  - 200: Success
  - 404: Task not found

#### PATCH /api/{user_id}/tasks/{task_id}/toggle
- Description: Toggle completion status of a task
- Response: Updated Task object
- Status Codes:
  - 200: Success
  - 404: Task not found

### Authentication

#### POST /api/auth/login
- Description: Authenticate user and return token
- Request Body: Login credentials
- Response: Authentication token
- Status Codes:
  - 200: Success
  - 401: Invalid credentials

#### POST /api/auth/register
- Description: Register new user
- Request Body: Registration data
- Response: Authentication token
- Status Codes:
  - 201: Created
  - 400: Invalid request data

## Task Object Structure
- id: Numeric identifier for the task
- user_id: ID of the user who owns the task
- title: Task title
- description: Task description
- completed: Boolean indicating completion status
- created_at: Timestamp of creation
- updated_at: Timestamp of last update

## Error Responses
- 400: Bad Request - Invalid request format
- 401: Unauthorized - Not authenticated
- 403: Forbidden - Access denied
- 404: Not Found - Resource not found
- 500: Internal Server Error - Unexpected error