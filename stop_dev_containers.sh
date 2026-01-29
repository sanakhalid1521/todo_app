#!/bin/bash
# Script to stop Todo App development containers

echo "Stopping Todo App development containers..."

# Stop the development containers
docker compose -f docker-compose.desktop.yml down

echo "Containers stopped successfully."