@echo off
REM Script to start Todo App development containers with bind mounts and watch mode

echo Starting Todo App development containers with bind mounts...
echo This will create containers with live reload capability for both frontend and backend.

REM Check if Docker is running
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not installed or not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker compose version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker Compose is not available. Please ensure Docker Desktop includes Compose.
    pause
    exit /b 1
)

echo.
echo Building and starting development containers with bind mounts...
echo Frontend will be available at http://localhost:3001
echo Backend will be available at http://localhost:8000
echo.
echo Press Ctrl+C to stop the containers

REM Start the development containers with bind mounts and watch mode
docker compose -f docker-compose.desktop.yml up --build

pause