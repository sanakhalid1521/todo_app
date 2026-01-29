#!/bin/bash
# Script to manage the Todo App Docker containers with frontend, backend, and chatbot

echo "Starting Todo App Services with Docker Compose..."

# Check if Docker is installed and running
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed or not in PATH. Please install Docker Desktop first."
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "Docker daemon is not running. Please start Docker Desktop."
    exit 1
fi

echo "Building and starting all services (frontend, backend, chatbot) with bind mounts and watch mode..."
echo "Press Ctrl+C to stop the containers later."

# Start the services using the fixed docker-compose file with all services
docker-compose -f docker-compose.fixed.yml up --build

echo
echo "All services stopped."
echo "To start again, run this script again."