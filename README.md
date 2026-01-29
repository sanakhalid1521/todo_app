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
- Complete deployment scripts for Linux/Mac/Windows
- AI Chatbot functionality fully preserved in Kubernetes

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

### Prerequisites

- Docker Desktop with Kubernetes enabled
- Helm 3.x
- kubectl
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- Neon database account (free tier available)

### Quick Start with Docker Compose

```bash
# Copy environment file
cp .env.example .env
# Update .env with your actual values

# Start the application
docker-compose up --build
```

### Kubernetes Deployment

```bash
# For development (with bind mounts and hot reload)
helm install todo-app ./k8s/helm -f k8s/helm/values.dev.yaml

# For production
helm install todo-app ./k8s/helm
```

## 🤖 AI Chatbot Features

The application includes an AI-powered chatbot that understands natural language commands:

### Supported Commands

- **English**: "Add task: buy groceries", "Show my tasks", "Mark task 1 as complete"
- **Roman Urdu**: "Task bnao: submit assignment", "Mere tasks dikhao", "Task 1 complete kro"

### API Endpoints

- **Chat Endpoint**: `POST /api/chat/message`
- **Swagger UI**: `GET /docs`

## 🐛 Troubleshooting

If you encounter issues:

1. **Chatbot errors**: Check the [Chatbot Troubleshooting Guide](CHATBOT_TROUBLESHOOTING.md)
2. **Database connection**: Verify your Neon database URL in `.env`
3. **Kubernetes**: Use `kubectl logs -f deployment/backend-deployment -n todo-app` to check logs

## Development Guidelines

This project follows spec-driven development methodology. All implementations should reference the specifications in the `/specs` directory. When implementing new features, follow the established patterns and maintain consistency with the existing architecture.

## 🚀 Deployment

The application is designed for containerized deployment with:

- **Docker Compose**: For local development and testing
- **Kubernetes**: For production deployment with Helm charts
- **Neon Database**: Serverless PostgreSQL for automatic scaling
- **Auto-scaling**: Horizontal Pod Autoscalers for dynamic scaling