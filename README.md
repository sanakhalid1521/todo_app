# Todo App - 5-Phase Evolution Project

This project implements the complete 5-phase evolution as outlined in Hackathon II, transforming from a simple console application to a cloud-native AI-powered system.

## Project Structure

```
hackathon-todo/
├── .specify/           # Spec-Kit configuration
│   └── config.yaml
├── specs/             # Spec-Kit managed specifications
│   ├── overview.md
│   ├── architecture.md
│   ├── features/
│   │   ├── task-crud.md
│   │   ├── authentication.md
│   │   └── chatbot.md
│   ├── api/
│   │   └── rest-endpoints.md
│   ├── database/
│   │   └── schema.md
│   └── ui/
│       ├── components.md
│       └── pages.md
├── .claude/           # Reusable intelligence (agents and skills)
│   ├── agents/
│   └── skills/
├── frontend/          # Next.js application
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── ...
├── backend/           # FastAPI application
│   ├── api/
│   ├── crud/
│   ├── schemas/
│   ├── database.py
│   └── main.py
├── CLAUDE.md          # Claude Code instructions
├── docker-compose.yml
└── README.md
```

## Phases

### Phase I: In-Memory Python Console App
- Basic todo functionality in Python console
- In-memory storage
- Core CRUD operations

### Phase II: Full-Stack Web Application (Current)
- Next.js frontend with App Router
- FastAPI backend with SQLModel
- Neon Serverless Database
- Complete task management features

### Phase III: AI-Powered Todo Chatbot
- Natural language processing
- OpenAI ChatKit integration
- Conversational task management

### Phase IV: Local Kubernetes Deployment (Completed)
- Containerization with Docker (Multi-stage builds)
- Local deployment on Minikube
- Helm charts for orchestration
- Production-grade Kubernetes manifests
- Monitoring stack with Prometheus and Grafana
- Security configurations (Network Policies, RBAC)
- Auto-scaling with Horizontal Pod Autoscalers
- AI-assisted deployment tools (kubectl-ai, Kagent, Docker AI Agent)

### Phase V: Advanced Cloud Deployment
- Production deployment on DigitalOcean Kubernetes
- Event-driven architecture with Kafka and Dapr

## Features Implemented (Phase II)

### Basic Features
- [x] Add Task – Create new todo items
- [x] Delete Task – Remove tasks from the list
- [x] Update Task – Modify existing task details
- [x] View Task List – Display all tasks
- [x] Mark as Complete – Toggle task completion status

### Intermediate Features
- [x] Priorities & Tags/Categories – Assign levels and labels
- [x] Search & Filter – Search by keyword; filter by status
- [x] Sort Tasks – Reorder by due date, priority, or alphabetically

### Advanced Features
- [x] Due Dates & Time Reminders – Set deadlines with date/time pickers
- [ ] Recurring Tasks – Auto-reschedule repeating tasks

## Technology Stack

### Frontend
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- Lucide React Icons

### Backend
- FastAPI
- SQLModel
- SQLAlchemy
- Pydantic

### Database
- Neon Serverless PostgreSQL
- UUID primary keys
- AsyncSession for database operations

### Development
- Spec-Driven Development
- Claude Code integration
- Reusable Intelligence (Agents & Skills)

## Getting Started

1. Clone the repository
2. Navigate to the frontend directory and install dependencies: `npm install`
3. Navigate to the backend directory and install dependencies: `pip install -r requirements.txt`
4. Start the development servers for both frontend and backend

## Development Guidelines

This project follows spec-driven development methodology. All implementations should reference the specifications in the `/specs` directory. When implementing new features, follow the established patterns and maintain consistency with the existing architecture.