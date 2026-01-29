@echo off
REM Script to manage the Todo App Docker containers with frontend, backend, and chatbot

echo Starting Todo App Services with Docker Compose...

REM Check if Docker is installed and running
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not installed or not in PATH. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker daemon is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker daemon is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

echo Building and starting all services (frontend, backend, chatbot) with bind mounts and watch mode...
echo Press Ctrl+C to stop the containers later.

REM Start the services using the fixed docker-compose file with all services
docker-compose -f docker-compose.fixed.yml up --build

echo.
echo All services stopped.
echo To start again, run this script again.
echo.
pause