#!/bin/bash
# Docker diagnostic script for Todo App

echo "🔍 Docker Diagnostic for Todo App"
echo "================================="

echo "📋 Checking environment variables in Docker..."
if [ -f .env ]; then
    echo "✅ .env file found"
    echo "Current DATABASE_URL setting:"
    grep DATABASE_URL .env || echo "❌ DATABASE_URL not found in .env"
    echo ""
else
    echo "❌ .env file not found!"
    echo "Please create a .env file with your database configuration"
    exit 1
fi

echo "🐳 Checking if Docker containers are running..."
docker ps

echo ""
echo "📊 Checking backend container logs..."
if docker ps | grep -q "todo-app-backend"; then
    echo "Getting backend logs..."
    docker logs todo-app-backend --tail 50
elif docker ps | grep -q "todo-app-backend-dev"; then
    echo "Getting backend development logs..."
    docker logs todo-app-backend-dev --tail 50
else
    echo "⚠️  Backend container not found. Checking for any running containers..."
    docker ps -a
fi

echo ""
echo "🔧 Testing database connection inside container..."
if docker ps | grep -q "todo-app-backend"; then
    echo "Testing connection in todo-app-backend container..."
    docker exec todo-app-backend python -c "
import os
from dotenv import load_dotenv
from backend.database import test_connection
import asyncio

load_dotenv('.env')
print('DATABASE_URL from container:', os.getenv('DATABASE_URL', 'NOT SET'))
success = asyncio.run(test_connection())
print('Connection test result:', success)
"
elif docker ps | grep -q "todo-app-backend-dev"; then
    echo "Testing connection in todo-app-backend-dev container..."
    docker exec todo-app-backend-dev python -c "
import os
from dotenv import load_dotenv
from backend.database import test_connection
import asyncio

load_dotenv('.env')
print('DATABASE_URL from container:', os.getenv('DATABASE_URL', 'NOT SET'))
success = asyncio.run(test_connection())
print('Connection test result:', success)
"
else
    echo "⚠️  No running backend container found to test"
fi

echo ""
echo "💡 Common Docker Issues and Solutions:"
echo "1. Make sure your .env file has the correct database credentials"
echo "2. Ensure the database URL is accessible from inside the container"
echo "3. For Neon, make sure your IP is whitelisted in Neon console"
echo "4. Check that the container can reach the internet to connect to Neon"
echo ""
echo "📝 To rebuild with new environment variables:"
echo "   docker-compose down && docker-compose up --build"
echo ""
echo "🔍 To check container environment:"
echo "   docker exec -it [container_name] env | grep DATABASE"