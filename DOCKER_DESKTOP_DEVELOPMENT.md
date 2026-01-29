# Todo App - Development with Docker Desktop

This guide explains how to run the Todo App in development mode using Docker Desktop with bind mounts and watch mode for real-time code changes.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)

## Running the Development Environment

### Windows
Run the following command to start the development containers:
```cmd
start_dev_containers.bat
```

### Linux/Mac
Run the following command to start the development containers:
```bash
./start_dev_containers.sh
```

## Features

- **Bind Mounts**: Source code is mounted directly from your host machine to the containers
- **Watch Mode**: Changes to your code are automatically reflected in the running containers
- **Live Reload**: Both frontend and backend support hot reloading during development
- **Development Optimized**: Configured with development-specific settings and dependencies

## Services

- **Frontend**: Available at `http://localhost:3001`
- **Backend**: Available at `http://localhost:8000`
- **Database**: PostgreSQL running on `localhost:5432`

## Stopping the Containers

### Windows
Run the following command to stop the containers:
```cmd
stop_dev_containers.bat
```

### Linux/Mac
Run the following command to stop the containers:
```bash
./stop_dev_containers.sh
```

## Configuration Details

The development environment is configured with:

- Hot reloading enabled for both frontend (Next.js) and backend (FastAPI)
- Volume mounts to prevent host files from interfering with container dependencies
- Proper environment variables for development
- Health checks to ensure services start in the correct order
- Isolated network for the application services

## Troubleshooting

If you encounter issues:

1. Ensure Docker Desktop is running with sufficient resources allocated
2. Check that no other applications are using ports 3001, 8000, or 5432
3. Verify that your `.env` file contains the necessary configuration values
4. Look at the container logs for specific error messages

## Docker Compose Files

- `docker-compose.desktop.yml`: Optimized for Docker Desktop development
- `docker-compose.dev.yml`: Alternative development configuration
- `docker-compose.yml`: Production-like configuration