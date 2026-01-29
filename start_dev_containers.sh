#!/bin/bash
# Script to start Todo App development containers with bind mounts and watch mode

echo "Starting Todo App development containers with bind mounts..."
echo "This will create containers with live reload capability for both frontend and backend."

# Check if Docker is running
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed or not running. Please start Docker Desktop first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker compose &> /dev/null; then
    echo "Docker Compose is not available. Please ensure Docker Desktop includes Compose."
    exit 1
fi

echo ""
echo "Building and starting development containers with bind mounts..."
echo "Frontend will be available at http://localhost:3001"
echo "Backend will be available at http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the containers"

# Start the development containers with bind mounts and watch mode
docker compose -f docker-compose.desktop.yml up --build