# Chatbot Troubleshooting Guide

This guide helps troubleshoot common issues with the AI chatbot functionality in the Todo app.

## Common Issues

### 1. "Sorry, I encountered an error processing your request" Error

This error typically occurs due to one of the following reasons:

#### A. Database Connection Issues
- **Symptoms**: Error occurs when trying to add/list/update tasks
- **Causes**:
  - Incorrect database URL in environment variables
  - Database server is down or unreachable
  - Invalid credentials for Neon database
- **Solution**:
  ```bash
  # Verify your database URL is correct
  echo $DATABASE_URL

  # Test database connection (from backend directory)
  python -c "from database import test_connection; import asyncio; asyncio.run(test_connection())"
  ```

#### B. OpenAI API Key Issues
- **Symptoms**: Error occurs immediately when sending any message
- **Causes**:
  - Missing or invalid OpenAI API key
  - Insufficient API quota
  - Network connectivity issues to OpenAI
- **Solution**:
  ```bash
  # Verify API key is set
  echo $OPENAI_API_KEY

  # Check if API key is valid by making a simple request
  curl -H "Authorization: Bearer $OPENAI_API_KEY" \
       -H "Content-Type: application/json" \
       https://api.openai.com/v1/models
  ```

#### C. Model Permission Issues
- **Symptoms**: Error occurs consistently for specific operations
- **Causes**: Account doesn't have access to required GPT models
- **Solution**: Ensure your OpenAI account has access to gpt-3.5-turbo or gpt-4

### 2. Specific Task Operation Failures

#### "Add book" Command Fails
- **Problem**: The chatbot tries to interpret "add book" as a task operation
- **Solution**: The chatbot is designed for task management. For "add book", try more specific commands like:
  - "Add task: buy books"
  - "Create a task to buy books"
  - "Remember to buy books"

#### Database Schema Issues
- **Problem**: Table creation failures or missing columns
- **Solution**: Ensure the database tables are properly created:
  ```bash
  # From backend directory, initialize the database
  python -c "from database import init_db; import asyncio; asyncio.run(init_db())"
  ```

## Debugging Steps

### 1. Check Environment Variables
```bash
# Verify all required environment variables are set
cat .env
```

### 2. Test Database Connection
```bash
# Test the database connection directly
cd backend
python -c "
import os
from dotenv import load_dotenv
from database import test_connection
import asyncio

load_dotenv()
asyncio.run(test_connection())
"
```

### 3. Check Application Logs
```bash
# If running with Docker Compose
docker-compose logs backend

# If running with Kubernetes
kubectl logs -f deployment/backend-deployment -n todo-app
```

### 4. Verify Chat Route is Available
- Access `http://localhost:8000/docs` to see available API routes
- Look for `/api/chat/message` endpoint
- Test the endpoint directly using the Swagger UI

## Database Models Used by Chatbot

The chatbot uses these database models:
- `Task` (for todo operations)
- `ConversationSession` (for conversation history)
- `ConversationMessage` (for individual messages)

## Sample Working Commands

These commands should work with the chatbot:

### Task Management
- "Add task: buy groceries"
- "Create a task to call mom"
- "Show my tasks"
- "List pending tasks"
- "Mark task 1 as complete"
- "Delete task 2"

### English and Roman Urdu Support
- "Task bnao: submit assignment"
- "Mere tasks dikhao"
- "Task 1 complete kro"

## Configuration Requirements

### For Neon Database
```env
DATABASE_URL=postgresql://username:password@ep-xxxxxx.region.aws.neon.tech/dbname?sslmode=require
```

### For OpenAI
```env
OPENAI_API_KEY=sk-...your-api-key-here...
```

### Authentication
```env
BETTER_AUTH_SECRET=your-32-character-secret-key-here
```

## Testing the Chatbot Functionality

You can test the chat functionality directly with curl:

```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add task: buy milk",
    "user_id": "test-user",
    "session_id": "test-session"
  }'
```

## Recovery Steps

If the chatbot stops working:

1. Restart the backend service
2. Verify database connection
3. Check OpenAI API key validity
4. Clear conversation history if needed
5. Test with simple commands first

## Development Mode Debugging

When developing, enable debug output by adding these to your environment:
```env
LOG_LEVEL=debug
ENVIRONMENT=development
```

This will provide more detailed error messages in the logs.