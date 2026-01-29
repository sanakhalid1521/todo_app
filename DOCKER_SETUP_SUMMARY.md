# Docker Setup for Todo App - Running Services

Congratulations! Your Docker containers for the Todo App are now running. Here's the breakdown of the running services:

## Running Containers

1. **Database Service**
   - Container Name: `todo-app-postgres-new`
   - Image: `postgres:15`
   - Port: `5433` (mapped from container port 5432)
   - Database: `todo_app`
   - User: `postgres`

2. **Backend Service**
   - Container Name: `todo-app-backend-new`
   - Image: `todo-app-backend:latest`
   - Port: `8001` (mapped from container port 8000)
   - Health Status: Currently unhealthy (may have startup issues)

3. **Frontend Service**
   - Container Name: `todo-app-frontend-final`
   - Image: `todo-app-frontend:latest`
   - Port: `3001` (mapped from container port 3000)

## Access URLs

- **Frontend Application**: http://localhost:3001
- **Backend API**: http://localhost:8001
- **Backend API Documentation**: http://localhost:8001/docs

## Chatbot Component

The chatbot functionality is integrated into the frontend application. You can access it through the floating chat icon on the Todo app interface at http://localhost:3001.

## Database Connection

The backend is configured to connect to the PostgreSQL database using:
- Host: `localhost` (from host machine)
- Port: `5433`
- Database: `todo_app`
- Username: `postgres`
- Password: `postgres`

## Environment Configuration

The `.env` file is mounted in the backend container at `/app/.env` to provide the necessary environment variables including:
- `DATABASE_URL`
- `BETTER_AUTH_SECRET`
- `OPENAI_API_KEY`

## Bind Mounts (Watch Mode)

- Backend code is mounted at `/app` in the backend container for live reloading
- Frontend code is mounted at `/app` in the frontend container for live reloading
- Changes to the source code will be reflected in the running containers

## Troubleshooting

If the backend service shows as unhealthy, you can check its logs:
```
docker logs todo-app-backend-new
```

If the frontend service is not responding, check its logs:
```
docker logs todo-app-frontend-final
```

## Stopping the Services

To stop all services:
```
docker stop todo-app-postgres-new todo-app-backend-new todo-app-frontend-final
```

To remove the containers:
```
docker rm todo-app-postgres-new todo-app-backend-new todo-app-frontend-final
```

## Docker Compose File

The configuration used is in `docker-compose-run.yml` which sets up:
- Network connectivity between services
- Port mappings to avoid conflicts
- Volume mounts for development
- Environment variable configuration