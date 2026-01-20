# Quickstart Guide: Kubernetes Deployment for AI Chatbot Application

## Prerequisites

- Docker Desktop with Kubernetes enabled OR Minikube installed
- kubectl command-line tool
- Helm 3.x (optional, for advanced deployments)
- Node.js and npm (for local development)
- Git

## Option 1: Using Minikube (Local Development)

### 1. Start Minikube

```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --disk-size=40g

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server
```

### 2. Set Docker environment to Minikube

```bash
# Point Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)
```

### 3. Build Docker Images

```bash
# Build backend image
cd backend
docker build -t todo-backend:latest .

# Build frontend image
cd ../frontend
docker build -t todo-frontend:latest .
```

### 4. Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace todo-app

# Apply Kubernetes manifests
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
kubectl apply -f k8s/ingress.yaml

# Wait for deployments to be ready
kubectl wait --for=condition=ready pod -l app=backend -n todo-app
kubectl wait --for=condition=ready pod -l app=frontend -n todo-app
```

### 5. Access the Application

```bash
# Get Minikube IP
minikube ip

# Access via ingress
minikube tunnel  # Run in separate terminal
# Then access http://todo-app.local in browser
```

## Option 2: Using Standard Kubernetes Cluster

### 1. Build and Push Images

```bash
# Tag and push images to your container registry
docker build -t your-registry/todo-backend:latest ./backend
docker push your-registry/todo-backend:latest

docker build -t your-registry/todo-frontend:latest ./frontend
docker push your-registry/todo-frontend:latest
```

### 2. Configure Secrets

```bash
# Create secrets for database and API keys
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="your-database-url" \
  --from-literal=OPENAI_API_KEY="your-openai-api-key" \
  --from-literal=BETTER_AUTH_SECRET="your-auth-secret" \
  -n todo-app
```

### 3. Deploy Application

```bash
# Apply all manifests
kubectl apply -f k8s/ -n todo-app
```

## Configuration

### Environment Variables

The application requires the following environment variables:

**Backend:**
- `DATABASE_URL`: Connection string for NeonDB
- `OPENAI_API_KEY`: API key for OpenAI integration
- `BETTER_AUTH_SECRET`: Secret key for authentication
- `JWT_ALGORITHM`: Algorithm for JWT (default: HS256)
- `JWT_EXPIRATION_DAYS`: JWT expiration (default: 7)
- `CORS_ORIGINS`: Allowed origins for CORS (comma-separated)

**Frontend:**
- `NEXT_PUBLIC_API_BASE_URL`: URL of the backend API
- `NEXT_PUBLIC_AUTH_SECRET`: Auth secret for frontend

### Ingress Configuration

The application uses NGINX Ingress to route traffic:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: todo-app.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 3000
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8000
```

## Monitoring and Logging

### Check Pod Status

```bash
# View all pods
kubectl get pods -n todo-app

# View pod logs
kubectl logs -f deployment/backend-deployment -n todo-app
kubectl logs -f deployment/frontend-deployment -n todo-app
```

### Health Checks

```bash
# Check service endpoints
kubectl get endpoints -n todo-app

# Check ingress status
kubectl get ingress -n todo-app
```

## Scaling

### Manual Scaling

```bash
# Scale backend deployment
kubectl scale deployment backend-deployment --replicas=3 -n todo-app

# Scale frontend deployment
kubectl scale deployment frontend-deployment --replicas=3 -n todo-app
```

### Auto Scaling with HPA

```bash
# Create Horizontal Pod Autoscaler
kubectl autoscale deployment backend-deployment --cpu-percent=70 --min=1 --max=10 -n todo-app
kubectl autoscale deployment frontend-deployment --cpu-percent=70 --min=1 --max=5 -n todo-app
```

## Cleanup

```bash
# Delete all resources
kubectl delete namespace todo-app

# Stop Minikube (if using)
minikube stop
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
```