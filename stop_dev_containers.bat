@echo off
REM Script to stop Todo App development containers

echo Stopping Todo App development containers...

REM Stop the development containers
docker compose -f docker-compose.desktop.yml down

echo Containers stopped successfully.
pause