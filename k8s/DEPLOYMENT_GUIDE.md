# Deployment Guide: Todo AI Chatbot Application

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start with Helm](#quick-start-with-helm)
3. [Manual Kubernetes Deployment](#manual-kubernetes-deployment)
4. [Configuration](#configuration)
5. [Monitoring and Observability](#monitoring-and-observability)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

- Kubernetes cluster (v1.20 or higher)
- Helm 3.x
- kubectl
- Docker (for building images)

## Quick Start with Helm

### 1. Add the repository and install

```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Create the namespace
kubectl create namespace todo-app

# Install the application using Helm
helm install todo-app ./k8s/helm --namespace todo-app --set secrets.databaseUrl="<BASE64_ENCODED_DB_URL>" --set secrets.openaiApiKey="<BASE64_ENCODED_OPENAI_KEY>" --set secrets.authSecret="<BASE64_ENCODED_AUTH_SECRET>"
```

## Development vs Production Considerations

### Bind Mounts and Local Development
- **Development**: Docker Compose files use bind mounts for live reloading during development
- **Production/Kubernetes**: No bind mounts are used as they are not suitable for containerized environments
- **Dockerfiles**: Different Dockerfiles are provided for different environments:
  - `Dockerfile.dev`: For development with live reload capabilities
  - `Dockerfile.prod`: For production with optimized builds and no bind mounts

### 2. Verify the installation

```bash
# Check the status
helm status todo-app --namespace todo-app

# List all resources
kubectl get all -n todo-app

# Check pod status
kubectl get pods -n todo-app
```

## Manual Kubernetes Deployment

### 1. Create the namespace

```bash
kubectl create namespace todo-app
```

### 2. Create secrets

```bash
# Create secrets for the application
kubectl create secret generic todo-app-secrets \
  --from-literal=DATABASE_URL="<your-base64-encoded-db-url>" \
  --from-literal=OPENAI_API_KEY="<your-base64-encoded-openai-key>" \
  --from-literal=BETTER_AUTH_SECRET="<your-base64-encoded-auth-secret>" \
  -n todo-app
```

### 3. Deploy the application

```bash
# Apply all Kubernetes manifests
kubectl apply -f k8s/configmap.yaml -n todo-app
kubectl apply -f k8s/backend-deployment.yaml -n todo-app
kubectl apply -f k8s/frontend-deployment.yaml -n todo-app
kubectl apply -f k8s/ingress.yaml -n todo-app
kubectl apply -f k8s/network-policy.yaml -n todo-app
kubectl apply -f k8s/rbac.yaml -n todo-app
kubectl apply -f k8s/hpa.yaml -n todo-app
```

## Configuration

### Environment Variables

#### Backend
- `DATABASE_URL`: Connection string for the database
- `OPENAI_API_KEY`: API key for OpenAI integration
- `BETTER_AUTH_SECRET`: Secret key for authentication
- `JWT_ALGORITHM`: Algorithm for JWT (default: HS256)
- `JWT_EXPIRATION_DAYS`: JWT expiration (default: 7)
- `CORS_ORIGINS`: Allowed origins for CORS (comma-separated)

#### Frontend
- `NEXT_PUBLIC_API_BASE_URL`: URL of the backend API
- `NEXT_PUBLIC_AUTH_SECRET`: Auth secret for frontend

### Scaling Configuration

The application supports both manual and automatic scaling:

```bash
# Manual scaling
kubectl scale deployment backend-deployment --replicas=3 -n todo-app
kubectl scale deployment frontend-deployment --replicas=3 -n todo-app

# Check HPA status
kubectl get hpa -n todo-app
```

## Monitoring and Observability

### Prometheus and Grafana

To deploy the monitoring stack:

```bash
# Create monitoring namespace
kubectl create namespace monitoring

# Deploy monitoring components
kubectl apply -f k8s/monitoring/namespace.yaml
kubectl apply -f k8s/monitoring/prometheus-config.yaml
kubectl apply -f k8s/monitoring/grafana-deployment.yaml
kubectl apply -f k8s/monitoring/service-monitor.yaml
```

### Health Checks

Check the health of your deployments:

```bash
# Check pod status
kubectl get pods -n todo-app

# Check service status
kubectl get svc -n todo-app

# Check logs
kubectl logs -f deployment/backend-deployment -n todo-app
kubectl logs -f deployment/frontend-deployment -n todo-app
```

## Troubleshooting

### Common Issues

1. **Images not found**: Ensure you've built images in the correct Docker environment
2. **Services not accessible**: Check ingress controller is running and configured
3. **Database connection errors**: Verify database connection string in secrets
4. **API key errors**: Confirm OpenAI API key is properly configured

### Debugging Commands

```bash
# Describe pod for detailed status
kubectl describe pod <pod-name> -n todo-app

# Check service configuration
kubectl describe service <service-name> -n todo-app

# Port forward for direct access (for debugging)
kubectl port-forward service/backend-service 8000:8000 -n todo-app
kubectl port-forward service/frontend-service 3000:3000 -n todo-app

# Check ingress status
kubectl get ingress -n todo-app
```

### Cleaning Up

```bash
# Uninstall Helm release
helm uninstall todo-app --namespace todo-app

# Or delete all resources manually
kubectl delete namespace todo-app

# Delete monitoring stack
kubectl delete namespace monitoring
```

## Security Best Practices

- Always use secrets for sensitive data (API keys, database credentials)
- Implement network policies to restrict traffic between services
- Use RBAC to limit permissions for application pods
- Regularly rotate secrets
- Use secure base images for Docker builds
- Implement proper health checks and liveness probes