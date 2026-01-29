@echo off
REM Docker diagnostic script for Todo App

echo 🔍 Docker Diagnostic for Todo App
echo =================================

echo 📋 Checking environment variables in Docker...
if exist ".env" (
    echo ✅ .env file found
    echo Current DATABASE_URL setting:
    findstr DATABASE_URL .env
    echo.
) else (
    echo ❌ .env file not found!
    echo Please create a .env file with your database configuration
    exit /b 1
)

echo 🐳 Checking if Docker containers are running...
docker ps

echo.
echo 📊 Checking backend container logs...
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" > temp_containers.txt
findstr /C:"todo-app-backend" temp_containers.txt >nul
if %errorlevel% == 0 (
    echo Getting backend logs...
    docker logs todo-app-backend --tail 50
) else (
    findstr /C:"todo-app-backend-dev" temp_containers.txt >nul
    if %errorlevel% == 0 (
        echo Getting backend development logs...
        docker logs todo-app-backend-dev --tail 50
    ) else (
        echo ⚠️  Backend container not found. Checking for any running containers...
        docker ps -a
    )
)

del temp_containers.txt

echo.
echo 💡 Common Docker Issues and Solutions:
echo 1. Make sure your .env file has the correct database credentials
echo 2. Ensure the database URL is accessible from inside the container
echo 3. For Neon, make sure your IP is whitelisted in Neon console
echo 4. Check that the container can reach the internet to connect to Neon
echo.
echo 📝 To rebuild with new environment variables:
echo    docker-compose down ^&^& docker-compose up --build
echo.
echo 🔍 To check container environment:
echo    docker exec -it [container_name] env ^| findstr DATABASE

pause