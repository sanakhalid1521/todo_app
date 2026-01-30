# Implementation Plan: Phase V - Cloud Deployment with Advanced Features

## Overview
Transform the Kubernetes-deployed application into a production cloud application with CI/CD, advanced search/filter, real-time updates, and optional bonus features. This phase deploys the Phase IV application to production cloud infrastructure and adds advanced features that make it a complete, production-ready SaaS application.

## Prerequisites
- Completed Phase IV (Kubernetes containerization)
- GitHub repository access
- Vercel account for frontend deployment
- Railway/Render account for backend deployment
- Neon PostgreSQL database access

## Implementation Steps

### Phase 1: Environment Setup and Configuration

#### 1.1 Repository Preparation
- Create `005-cloud-deployment` branch from `004-kubernetes-containerization`
- Update project documentation to reflect Phase V objectives
- Ensure all Phase IV functionality is working correctly

#### 1.2 Frontend Configuration (Vercel)
- Update `frontend/vercel.json` with production settings:
```json
{
  "version": 2,
  "name": "todo-frontend",
  "public": false,
  "framework": "nextjs",
  "env": {
    "NEXT_PUBLIC_API_URL": "@api-url",
    "BETTER_AUTH_SECRET": "@better-auth-secret",
    "NEXT_PUBLIC_SENTRY_DSN": "@sentry-dsn"
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "no-store, max-age=0"
        }
      ]
    }
  ]
}
```
- Configure environment variables in Vercel dashboard:
  - `NEXT_PUBLIC_API_URL`: Backend URL
  - `BETTER_AUTH_SECRET`: Auth secret
  - `NEXT_PUBLIC_SENTRY_DSN`: Sentry DSN

#### 1.3 Backend Configuration (Railway/Render)
- Create `railway.json` or `render.yaml`:
```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "docker/backend.Dockerfile"
  },
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```
- Configure environment variables:
  - `DATABASE_URL`: Neon connection string
  - `OPENAI_API_KEY`: OpenAI API key
  - `BETTER_AUTH_SECRET`: Same as frontend
  - `JWT_SECRET`: JWT signing key
  - `CORS_ORIGINS`: Vercel frontend URL
  - `SENTRY_DSN`: Sentry backend DSN

### Phase 2: Advanced Search Implementation

#### 2.1 Backend Search API
- Create `/api/{user_id}/tasks/search` endpoint
- Implement PostgreSQL ILIKE query for case-insensitive search
- Add debouncing (300ms) on the backend to handle frequent requests
- Return maximum 50 results per request
- Add highlighting of matched text in results

#### 2.2 Frontend Search Component
- Create `components/TaskSearch.tsx`
- Implement debounced input (300ms) using custom hook
- Highlight matching text in search results
- Add clear search button
- Display search statistics (results count)

### Phase 3: Advanced Filtering Implementation

#### 3.1 Backend Filter API
- Enhance existing task endpoints to support filtering parameters
- Add support for status, category, priority, and date range filters
- Implement combined AND filtering
- Add filter count calculations

#### 3.2 Frontend Filter Component
- Create `components/TaskFilters.tsx`
- Implement status filter (All/Pending/Completed)
- Implement category filter (checkboxes with counts)
- Implement priority filter (checkboxes with counts)
- Implement date filter (Overdue/Today/This Week/All)
- Add Apply/Clear buttons
- Persist filter state to localStorage

### Phase 4: Categories and Priorities Implementation

#### 4.1 Database Schema Updates
- Update `backend/app/models/task.py` to include category and priority fields:
```python
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.types import Enum as SQLEnum
import enum

class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Category(str, enum.Enum):
    WORK = "work"
    PERSONAL = "personal"
    SHOPPING = "shopping"
    HEALTH = "health"
    OTHER = "other"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=100, index=True)  # Index for search
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = Field(default=False, index=True)  # Index for filters

    # NEW FIELDS
    category: Category = Field(default=Category.OTHER, sa_column=Column(SQLEnum(Category)))
    priority: Priority = Field(default=Priority.MEDIUM, sa_column=Column(SQLEnum(Priority)))
    due_date: Optional[datetime] = Field(default=None, index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)
```

#### 4.2 Frontend Category and Priority Components
- Update `components/TaskCard.tsx` to show category badges and priority indicators
- Add color-coded category badges
- Add visual priority indicators (colors, icons)
- Update task creation/edit forms to include category and priority selection

### Phase 5: Due Date and Reminder Implementation

#### 5.1 Backend Due Date API
- Add due date field to task creation/update endpoints
- Implement date validation and formatting
- Create notification scheduling system for upcoming due dates

#### 5.2 Frontend Due Date Components
- Add date picker using react-datepicker
- Show relative time indicators ("Due in 2 days", "Overdue by 3 days")
- Add overdue styling (red) and due soon styling (yellow)
- Implement browser notifications with permission handling

### Phase 6: Real-Time Updates Implementation

#### 6.1 Server-Sent Events (SSE) Setup
- Create `/api/{user_id}/tasks/stream` endpoint for SSE
- Implement event broadcasting for task updates
- Handle connection management and reconnection logic

#### 6.2 Frontend Real-Time Updates
- Implement EventSource connection to SSE endpoint
- Handle optimistic UI updates with server confirmation
- Update task lists in real-time across tabs

### Phase 7: Bulk Operations Implementation

#### 7.1 Backend Bulk API
- Create `/api/{user_id}/tasks/bulk` endpoint
- Support bulk actions: complete, delete, change category, change priority
- Implement validation and error handling

#### 7.2 Frontend Bulk Operations UI
- Add checkbox selection for tasks
- Create bulk action dropdown
- Implement confirmation dialogs for destructive actions
- Add "Select all" and "Deselect all" functionality

### Phase 8: Analytics Dashboard Implementation

#### 8.1 Backend Stats API
- Create `/api/{user_id}/tasks/stats` endpoint
- Calculate statistics: total tasks, completed%, pending count, by category, by priority, overdue, etc.
- Implement date range filtering for historical data

#### 8.2 Frontend Dashboard
- Create `app/dashboard/page.tsx`
- Implement charts using Recharts library
- Create charts for:
  - Completion rate over time (line chart)
  - Tasks by category (pie chart)
  - Tasks by priority (bar chart)
  - Most productive days/times
- Add statistics cards with totals

### Phase 9: Export/Import Implementation

#### 9.1 Backend Export/Import API
- Create `/api/{user_id}/tasks/export` endpoint (CSV/JSON)
- Create `/api/{user_id}/tasks/import` endpoint (CSV/JSON)
- Implement validation and duplicate detection
- Add preview functionality for imports

#### 9.2 Frontend Data Management UI
- Create `components/DataManagement.tsx`
- Add export button that downloads CSV/JSON
- Add import button with file upload
- Implement preview and validation before import

### Phase 10: CI/CD Pipeline Implementation

#### 10.1 GitHub Actions Workflow
- Create `.github/workflows/ci.yml`:
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          cd backend
          pip install uv
          uv sync
      - name: Run tests
        run: |
          cd backend
          pytest
      - name: Lint
        run: |
          cd backend
          ruff check .

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      - name: Type check
        run: |
          cd frontend
          npm run type-check
      - name: Lint
        run: |
          cd frontend
          npm run lint
      - name: Build
        run: |
          cd frontend
          npm run build

  deploy-staging:
    if: github.ref == 'refs/heads/develop'
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: echo "Deploy to staging"

  deploy-production:
    if: github.ref == 'refs/heads/main'
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: echo "Deploy to production"
}
```

#### 10.2 Deployment Configuration
- Configure auto-deployment for main branch to production
- Configure auto-deployment for develop branch to staging
- Set up rollback capabilities

### Phase 11: Monitoring Setup

#### 11.1 Sentry Integration
- Frontend: Add to `frontend/lib/sentry.ts`:
```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
});
```
- Backend: Add to `backend/app/main.py`:
```python
import sentry_sdk

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("ENVIRONMENT", "production"),
    traces_sample_rate=1.0,
)
```

#### 11.2 Vercel Analytics
- Add to `frontend/app/layout.tsx`:
```typescript
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### Phase 12: Testing and Validation

#### 12.1 Unit Tests
- Add tests for new API endpoints
- Add tests for new components
- Update existing tests to accommodate new functionality

#### 12.2 End-to-End Tests
- Test all user scenarios with Playwright
- Verify all Phase I-IV functionality still works
- Test deployment process end-to-end

## Critical Files to Modify

### Backend Files:
- `backend/app/models/task.py` - Update task model with new fields
- `backend/app/routers/tasks.py` - Add search, filter, bulk endpoints
- `backend/app/routers/chat.py` - Ensure chatbot works with new features
- `backend/main.py` - Add Sentry integration
- `backend/database.py` - Update database initialization
- `backend/app/services/conversations.py` - Ensure compatibility

### Frontend Files:
- `frontend/components/TaskCard.tsx` - Update to show new fields
- `frontend/components/TaskSearch.tsx` - New search component
- `frontend/components/TaskFilters.tsx` - New filter component
- `frontend/components/DataManagement.tsx` - New export/import component
- `frontend/app/dashboard/page.tsx` - New dashboard page
- `frontend/app/tasks/page.tsx` - Update with new features
- `frontend/app/layout.tsx` - Add analytics
- `frontend/lib/sentry.ts` - Add Sentry configuration
- `frontend/lib/tasks-api.ts` - Update API client with new endpoints

### Configuration Files:
- `frontend/vercel.json` - Vercel configuration
- `railway.json` - Railway configuration
- `.github/workflows/ci.yml` - CI/CD workflow
- `.env.example` - Update environment variables

## Verification Steps

1. **Deployment Verification**:
   - Deploy frontend to Vercel successfully
   - Deploy backend to Railway/Render successfully
   - Verify all endpoints are accessible

2. **Feature Verification**:
   - Test search functionality with various queries
   - Test filtering by all available filters
   - Test category assignment and filtering
   - Test priority assignment and sorting
   - Test due date functionality and notifications
   - Test real-time updates across tabs
   - Test bulk operations
   - Test analytics dashboard
   - Test export/import functionality

3. **Integration Verification**:
   - Verify all Phase I-IV features still work
   - Test AI chatbot integration with new features
   - Verify authentication still works properly
   - Test error handling and edge cases

4. **Performance Verification**:
   - Verify page load times meet requirements (<2s)
   - Verify API response times (<500ms for 95%)
   - Verify real-time updates work smoothly (<1s latency)

5. **Monitoring Verification**:
   - Verify Sentry error tracking is working
   - Verify Vercel Analytics are collecting data
   - Verify health checks are passing