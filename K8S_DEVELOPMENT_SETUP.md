# Kubernetes Development Setup with Bind Mounts and Neon Database

This guide explains how to set up the Todo App with Kubernetes for development, including bind mounts for live code reloading and Neon database integration.

## Features

- **Bind Mounts**: Live code reloading for development
- **Watch Mode**: Auto-restart on file changes
- **Neon Database**: PostgreSQL database with serverless scaling
- **Chatbot Integration**: AI-powered chatbot functionality

## Prerequisites

- Docker Desktop with Kubernetes enabled
- Helm 3.x
- kubectl
- Neon database account (free tier available)

## Setup Steps

### 1. Configure Neon Database

1. Create a Neon account at https://neon.tech/
2. Create a new project
3. Get your connection string from the Neon dashboard
4. Update the `.env` file with your Neon database URL:

```bash
DATABASE_URL=postgresql://username:password@ep-your-project.region.aws.neon.tech/dbname?sslmode=require
OPENAI_API_KEY=your-actual-openai-api-key
BETTER_AUTH_SECRET=your-very-secure-32-character-secret-key-here-12345
```

### 2. Generate Base64 Encoded Secrets

Encode your secrets for Kubernetes:

```bash
# Encode your Neon database URL
echo -n "your-neon-database-url" | base64

# Encode your OpenAI API key
echo -n "your-openai-api-key" | base64

# Encode your auth secret
echo -n "your-auth-secret" | base64
```

Update `k8s/helm/values.dev.yaml` with the encoded values.

### 3. Development with Docker Compose

For quick development setup with Neon database:

```bash
# Using the development compose file with Neon
docker-compose -f docker-compose.dev-neon.yml up --build

# Or use the script to start everything
./setup_neon_config.sh
```

### 4. Development with Kubernetes

For Kubernetes development setup with bind mounts:

```bash
# Install the chart with development values
helm install todo-app ./k8s/helm -f k8s/helm/values.dev.yaml

# Or upgrade if already installed
helm upgrade todo-app ./k8s/helm -f k8s/helm/values.dev.yaml
```

### 5. Production Deployment

For production deployment without bind mounts:

```bash
# Install with default values (production)
helm install todo-app ./k8s/helm
```

## Development Workflow

### With Docker Compose (Recommended for Development)

1. Use `docker-compose.dev-neon.yml` for development
2. Code changes will automatically reload (watch mode)
3. Database persists with Neon's serverless scaling

### With Kubernetes (Advanced Development)

1. Update `values.dev.yaml` with your local paths for bind mounts
2. Deploy with Helm using dev values
3. Note: Kubernetes requires manual restart for code changes unless using advanced reload tools

## Troubleshooting

### Chatbot Not Working

1. Verify your OpenAI API key is correctly set in the environment
2. Check that the database connection is established
3. Ensure the chat router is properly imported in `main.py`

### Database Connection Issues

1. Confirm your Neon database URL is correct
2. Check that SSL mode is set to `require`
3. Verify network connectivity to Neon

### Bind Mount Issues

1. Ensure file permissions are correct
2. On Windows, ensure Docker Desktop shared drives are configured
3. Check that the paths in `values.dev.yaml` are accessible

## Files Overview

- `docker-compose.dev-neon.yml`: Docker Compose with Neon and live reload
- `k8s/helm/values.dev.yaml`: Development values for Kubernetes with bind mounts
- `k8s/helm/values.yaml`: Production values for Kubernetes
- `setup_neon_config.sh`: Linux/Mac setup script
- `setup_neon_config.bat`: Windows setup script
- `.env`: Environment variables (update with your actual values)

## Environment Variables

Update `.env` with your actual values:

```bash
DATABASE_URL=your-neon-database-url
OPENAI_API_KEY=your-openai-api-key
BETTER_AUTH_SECRET=your-auth-secret
```

## Commands Summary

```bash
# Development with Docker Compose
docker-compose -f docker-compose.dev-neon.yml up --build

# Development with Kubernetes
helm install todo-app ./k8s/helm -f k8s/helm/values.dev.yaml

# Production with Kubernetes
helm install todo-app ./k8s/helm

# Check status
kubectl get pods -n todo-app

# View logs
kubectl logs -f deployment/backend-deployment -n todo-app
```