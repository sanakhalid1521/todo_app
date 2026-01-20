# Docker Container Run Guide

This guide explains how to build and run your Todo app containers, including which terminal/command prompt to use.

## Terminal/Command Prompt Locations

### For Backend Container Operations:
- **Location**: Root directory (`E:\quarter-4\Hackathon-II\phase-1 todo\`)
- **Command Prompt**: Use the terminal in your root project directory

### For Frontend Container Operations:
- **Location**: Frontend directory (`E:\quarter-4\Hackathon-II\phase-1 todo\frontend`)
- **Command Prompt**: Use the terminal in the frontend directory

## Building Containers

### 1. Backend Container (Root Directory)
Open command prompt in the root directory and run:
```bash
# Build the backend container using the production Dockerfile
docker build -f Dockerfile.prod -t todo-backend .
```

### 2. Frontend Container (Frontend Directory)
Navigate to frontend directory and run:
```bash
cd frontend
# Build the frontend container using the Vercel-optimized Dockerfile
docker build -f Dockerfile.vercel -t todo-frontend .
```

## Running Containers

### Option 1: Separate Terminals (Recommended)
#### Terminal 1 (Root Directory - Backend):
```bash
# Navigate to root directory
cd "E:\quarter-4\Hackathon-II\phase-1 todo"

# Run backend container
docker run -d -p 8000:8000 \
  --name todo-backend \
  -e DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require" \
  -e BETTER_AUTH_SECRET="your-32-character-secret-key-here" \
  -e JWT_ALGORITHM="HS256" \
  -e JWT_EXPIRATION_DAYS="7" \
  -e CORS_ORIGINS="http://localhost:3000" \
  todo-backend
```

#### Terminal 2 (Frontend Directory - Frontend):
```bash
# Navigate to frontend directory
cd "E:\quarter-4\Hackathon-II\phase-1 todo\frontend"

# Run frontend container
docker run -d -p 3000:3000 \
  --name todo-frontend \
  -e NEXT_PUBLIC_API_BASE_URL="http://localhost:8000" \
  -e NEXT_PUBLIC_AUTH_SECRET="your-32-character-secret-key-here" \
  todo-frontend
```

### Option 2: Using Docker Compose (From Root Directory)
Create a docker-compose.yml file in the root directory:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.prod
    container_name: todo-backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
      BETTER_AUTH_SECRET: your-32-character-secret-key-here
      JWT_ALGORITHM: HS256
      JWT_EXPIRATION_DAYS: 7
      CORS_ORIGINS: http://localhost:3000
    networks:
      - todo-network

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.vercel
    container_name: todo-frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_BASE_URL: http://localhost:8000
      NEXT_PUBLIC_AUTH_SECRET: your-32-character-secret-key-here
    depends_on:
      - backend
    networks:
      - todo-network

networks:
  todo-network:
    driver: bridge
```

Then run from the root directory:
```bash
docker-compose up -d
```

## Quick Commands Summary

### From Root Directory:
```bash
# Build backend
docker build -f Dockerfile.prod -t todo-backend .

# Run backend
docker run -d -p 8000:8000 --name todo-backend -e DATABASE_URL="your-neon-url" todo-backend
```

### From Frontend Directory:
```bash
cd frontend

# Build frontend
docker build -f Dockerfile.vercel -t todo-frontend .

# Run frontend
docker run -d -p 3000:3000 --name todo-frontend -e NEXT_PUBLIC_API_BASE_URL="http://localhost:8000" todo-frontend
```

## Accessing Your Application

After running the containers:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Health check: http://localhost:8000/health

## Stopping Containers

### Individual containers:
```bash
# Stop frontend
docker stop todo-frontend
docker rm todo-frontend

# Stop backend
docker stop todo-backend
docker rm todo-backend
```

### Using Docker Compose:
```bash
# From root directory
docker-compose down
```

## Troubleshooting

### If containers fail to start:
1. Check environment variables are properly set
2. Verify your Neon database connection string
3. Make sure ports 3000 and 8000 are not in use
4. Check container logs: `docker logs todo-backend` or `docker logs todo-frontend`

### To check running containers:
```bash
docker ps
```

### To check container logs:
```bash
# From any directory
docker logs todo-backend  # for backend logs
docker logs todo-frontend  # for frontend logs
```

## Development with Bind Mounts

For development purposes, I've created special Dockerfiles that support bind mounts for live reloading:

### Development Dockerfiles:
- `Dockerfile.dev` (in root directory) - For backend development with live reload
- `frontend/Dockerfile.dev` (in frontend directory) - For frontend development with live reload
- `docker-compose.dev.yml` (in root directory) - For running both services with bind mounts

### To use bind mounts for development:

1. **Backend Development with Bind Mount:**
   ```bash
   # From root directory
   cd "E:\quarter-4\Hackathon-II\phase-1 todo"

   # Build development backend container
   docker build -f Dockerfile.dev -t todo-backend-dev .

   # Run with bind mount (any code changes will be reflected immediately)
   docker run -d -p 8000:8000 \
     --name todo-backend-dev \
     -e DATABASE_URL="sqlite:///./todo_app.db" \
     -e BETTER_AUTH_SECRET="your-32-character-secret-key-here" \
     -v ${PWD}/backend:/app/backend \
     -v ${PWD}/app.py:/app/app.py \
     todo-backend-dev
   ```

2. **Frontend Development with Bind Mount:**
   ```bash
   # From frontend directory
   cd "E:\quarter-4\Hackathon-II\phase-1 todo\frontend"

   # Build development frontend container
   docker build -f Dockerfile.dev -t todo-frontend-dev .

   # Run with bind mount (any code changes will be reflected immediately)
   docker run -d -p 3000:3000 \
     --name todo-frontend-dev \
     -e NEXT_PUBLIC_API_BASE_URL="http://localhost:8000" \
     -e NEXT_PUBLIC_AUTH_SECRET="your-32-character-secret-key-here" \
     -v ${PWD}:/app \
     todo-frontend-dev
   ```

3. **Using Docker Compose with Bind Mounts (Recommended for Development):**
   ```bash
   # From root directory - runs both services with bind mounts for live reloading
   docker-compose -f docker-compose.dev.yml up -d
   ```

### Benefits of Bind Mounts:
- Code changes are reflected immediately without rebuilding containers
- Faster development cycle
- Real-time debugging
- Persistent code changes across container restarts

### When to Use Each Approach:
- **Production Dockerfiles** (`Dockerfile.prod` and `Dockerfile.vercel`): For production deployments
- **Development Dockerfiles** (`Dockerfile.dev`): For local development with live reload
- **Bind Mounts**: During active development when you want to see code changes immediately
- **Regular Images**: For stable builds and production deployments