# Minikube Setup Guide for Todo AI Chatbot Application

This guide provides instructions for deploying the Todo AI Chatbot application on a local Minikube cluster as part of Phase IV: Kubernetes Containerization.

## Prerequisites

- Minikube installed (v1.20 or higher)
- kubectl
- Helm 3.x
- Docker Desktop with Gordon (Docker AI Agent) enabled (optional)
- kubectl-ai and Kagent (optional, for AI-assisted operations)

## Starting Minikube

```bash
# Start Minikube with sufficient resources
minikube start --memory=4096 --cpus=2

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server
```

## Option 1: Deploy using Helm (Recommended)

### 1. Prepare Base64-encoded secrets

```bash
# Replace with your actual values
export DATABASE_URL_B64=$(echo -n "postgresql://username:password@external-db:5432/todo_db" | base64)
export OPENAI_API_KEY_B64=$(echo -n "your-openai-api-key" | base64)
export AUTH_SECRET_B64=$(echo -n "your-32-char-auth-secret" | base64)
```

### 2. Create the namespace

```bash
kubectl create namespace todo-app
```

### 3. Deploy using Helm

```bash
cd k8s/helm
helm install todo-app . \
  --namespace todo-app \
  --set secrets.databaseUrl="$DATABASE_URL_B64" \
  --set secrets.openaiApiKey="$OPENAI_API_KEY_B64" \
  --set secrets.authSecret="$AUTH_SECRET_B64"
```

## Option 2: Deploy using AI-assisted tools (kubectl-ai and Kagent)

If you have kubectl-ai and Kagent installed:

```bash
# Using kubectl-ai for deployment
kubectl-ai "deploy the todo frontend with 2 replicas in todo-app namespace"
kubectl-ai "deploy the todo backend with 1 replica in todo-app namespace"
kubectl-ai "expose the frontend service on port 3000"

# Using Kagent for analysis
kagent "analyze the cluster health"
kagent "optimize resource allocation for the todo-app deployments"
```

## Option 3: Manual deployment

```bash
# Create namespace
kubectl create namespace todo-app

# Create secrets
kubectl create secret generic todo-app-secrets \
  --from-literal=DATABASE_URL="$(echo -n '<your-db-url>' | base64)" \
  --from-literal=OPENAI_API_KEY="$(echo -n '<your-openai-key>' | base64)" \
  --from-literal=BETTER_AUTH_SECRET="$(echo -n '<your-auth-secret>' | base64)" \
  -n todo-app

# Apply configurations
kubectl apply -f ../configmap.yaml -n todo-app
kubectl apply -f ../backend-deployment.yaml -n todo-app
kubectl apply -f ../frontend-deployment.yaml -n todo-app
kubectl apply -f ../ingress.yaml -n todo-app
kubectl apply -f ../hpa.yaml -n todo-app
kubectl apply -f ../network-policy.yaml -n todo-app
kubectl apply -f ../rbac.yaml -n todo-app
```

## Building Docker Images for Minikube

Before deploying, ensure Docker images are available in Minikube's container registry:

```bash
# Set Docker environment to Minikube
eval $(minikube docker-env)

# Build images
cd ../..  # From k8s/helm directory back to project root
docker build -t todo-backend:latest .
docker build -t todo-frontend:latest -f ./frontend/Dockerfile ./frontend

# Verify images are built
docker images | grep todo
```

## Verifying the Deployment

```bash
# Check all resources
kubectl get all -n todo-app

# Check pod status
kubectl get pods -n todo-app

# Check services
kubectl get svc -n todo-app

# Check logs
kubectl logs -f deployment/backend-deployment -n todo-app
kubectl logs -f deployment/frontend-deployment -n todo-app

# Access the application
minikube service frontend-service -n todo-app --url
```

## Scaling the Application

```bash
# Scale deployments manually
kubectl scale deployment backend-deployment --replicas=2 -n todo-app
kubectl scale deployment frontend-deployment --replicas=3 -n todo-app

# Check HPA status (if enabled)
kubectl get hpa -n todo-app
```

## Using Docker AI Agent (Gordon)

If Docker AI Agent (Gordon) is available in your region:

```bash
# Check Gordon's capabilities
docker ai "What can you do?"

# Use Gordon for Docker operations
docker ai "Build an optimized Docker image for the backend application"
docker ai "Create a multi-stage Dockerfile for the frontend with caching"
```

## Monitoring and Observability

Deploy the monitoring stack:

```bash
# Create monitoring namespace
kubectl create namespace monitoring

# Deploy monitoring components
kubectl apply -f ../monitoring/prometheus-config.yaml
kubectl apply -f ../monitoring/grafana-deployment.yaml
kubectl apply -f ../monitoring/service-monitor.yaml
```

## Troubleshooting

### Common Issues:

1. **Images not found**: Ensure you've run `eval $(minikube docker-env)` before building images
2. **Services not accessible**: Check if ingress controller is running: `kubectl get pods -n ingress-nginx`
3. **Database connection errors**: Verify database connection string in secrets
4. **API key errors**: Confirm OpenAI API key is properly configured

### Debugging Commands:

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

## Cleanup

```bash
# Uninstall Helm release
helm uninstall todo-app --namespace todo-app

# Or delete all resources manually
kubectl delete namespace todo-app

# Stop Minikube
minikube stop
```

## Integration Testing

Run the integration tests to verify the deployment:

```bash
chmod +x ../integration-test.sh
../integration-test.sh
```

## AIOps Recommendations

The deployment is designed to work with AI-assisted operations tools:

1. **kubectl-ai**: For intelligent Kubernetes operations
2. **Kagent**: For advanced cluster analysis and optimization
3. **Docker AI Agent (Gordon)**: For intelligent Docker operations

These tools can help optimize resource allocation, troubleshoot issues, and manage the deployment lifecycle more efficiently.