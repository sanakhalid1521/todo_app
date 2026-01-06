# Todo App Backend

This is the backend for the full-stack todo application built with FastAPI and Python.

## Features

- RESTful API for task management
- User authentication and authorization
- Database integration with SQLModel
- JWT-based authentication
- CRUD operations for tasks

## Tech Stack

- Python 3.13+
- FastAPI
- SQLModel
- PostgreSQL (with Neon)
- JWT for authentication
- Uvicorn for ASGI server

## Environment Variables

Create a `.env` file in the root of the backend directory with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
JWT_SECRET_KEY=your-super-secret-jwt-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
BETTER_AUTH_SECRET=your-better-auth-secret
CORS_ORIGINS=http://localhost:3000,https://*.vercel.app,https://*.vercel.com
```

## Getting Started

First, install the dependencies:

```bash
pip install -r requirements.txt
```

Or if using uv:

```bash
uv pip install -r requirements.txt
```

Then, run the development server:

```bash
uvicorn main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000).

## API Endpoints

- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{task_id}/toggle` - Toggle task completion status

## Database

The application uses SQLModel with PostgreSQL. The database schema is automatically created when the application starts.

## Authentication

Authentication is handled using JWT tokens. The API expects a Bearer token in the Authorization header for protected endpoints.

## Deploying

This application can be deployed to platforms like Heroku, Railway, or Vercel. Make sure to set the required environment variables in your deployment environment.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request