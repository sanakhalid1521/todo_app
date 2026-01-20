# Minikube Deployment Guide for Todo AI Chatbot Application

## Prerequisites

1. **Install Docker Desktop** (with Docker AI Agent - Gordon enabled)
   - Download and install Docker Desktop 4.53+
   - Enable Gordon: Go to Settings > Beta features > Toggle Docker AI Agent

2. **Install Minikube**
   ```bash
   # On Windows (using Chocolatey)
   choco install minikube

   # On macOS (using Homebrew)
   brew install minikube

   # On Linux
   curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
   sudo install minikube /usr/local/bin/
   ```

3. **Install kubectl**
   ```bash
   # On Windows (using Chocolatey)
   choco install kubernetes-cli

   # On macOS (using Homebrew)
   brew install kubernetes-cli

   # On Linux
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   ```

4. **Install kubectl-ai and Kagent**
   ```bash
   # Install kubectl-ai plugin
   kubectl krew install ai

   # Verify installation
   kubectl ai --help
   ```

5. **Install Helm**
   ```bash
   # On Windows
   choco install kubernetes-helm

   # On macOS
   brew install helm

   # On Linux
   curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
   ```

## Step 1: Start Minikube

```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --disk-size=40g

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard

# Verify Minikube is running
minikube status
```

## Step 2: Configure Docker to Use Minikube's Docker Daemon

```bash
# Point Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# On Windows PowerShell
minikube docker-env | Invoke-Expression
```

## Step 3: Build Docker Images Using Docker AI Agent (Gordon)

```bash
# Check Docker AI capabilities
docker ai "What can you do?"

# Navigate to project root
cd E:\quarter-4\Hackathon-II\phase-1 todo

# Build production-ready backend image using Docker AI
docker build -f backend/Dockerfile.prod -t todo-backend:latest ./backend

# Build production-ready frontend image using Docker AI
docker build -f frontend/Dockerfile.prod -t todo-frontend:latest ./frontend

# Verify images were built
docker images | grep todo-
```

## Understanding Docker Compose Files

Different docker-compose files are provided for different environments:

- `docker-compose.yml` - Development environment with Dockerfile.dev (contains bind mounts for live development)
- `docker-compose.prod.yml` - Production-like environment with Dockerfile.prod (no bind mounts, optimized for production)
- `docker-compose.dev.yml` - Alternative development setup with live reload capabilities

## Step 4: Deploy Using kubectl-ai and Kagent

### Option 1: Using kubectl-ai for deployment

```bash
# Create namespace using kubectl-ai
kubectl-ai "create namespace todo-app"

# Deploy using Helm (kubectl-ai can help with this too)
kubectl-ai "apply all resources from k8s/ directory"
```

### Option 2: Traditional deployment with AI assistance

```bash
# Create namespace
kubectl create namespace todo-app

# Create secrets (replace with your actual encoded values)
kubectl create secret generic todo-app-secrets \
  --from-literal=DATABASE_URL="your-base64-encoded-db-url" \
  --from-literal=OPENAI_API_KEY="your-base64-encoded-openai-key" \
  --from-literal=BETTER_AUTH_SECRET="your-base64-encoded-auth-secret" \
  -n todo-app

# Apply all Kubernetes manifests
kubectl apply -f k8s/configmap.yaml -n todo-app
kubectl apply -f k8s/backend-deployment.yaml -n todo-app
kubectl apply -f k8s/frontend-deployment.yaml -n todo-app
kubectl apply -f k8s/ingress.yaml -n todo-app
kubectl apply -f k8s/hpa.yaml -n todo-app
kubectl apply -f k8s/network-policy.yaml -n todo-app
kubectl apply -f k8s/rbac.yaml -n todo-app
```

## Step 5: Deploy Using Helm with AI Assistance

```bash
# Navigate to Helm chart directory
cd k8s/helm

# Deploy using Helm with kubectl-ai assistance
helm install todo-app . --namespace todo-app \
  --set secrets.databaseUrl="your-base64-encoded-db-url" \
  --set secrets.openaiApiKey="your-base64-encoded-openai-key" \
  --set secrets.authSecret="your-base64-encoded-auth-secret"

# Or use kubectl-ai to help with Helm commands
kubectl-ai "install helm chart todo-app with these secrets"
```

## Step 6: Monitor Deployment with AI Tools

```bash
# Check deployment status
kubectl get pods -n todo-app

# Use kubectl-ai to analyze the cluster
kubectl-ai "check why the pods are failing"  # if there are issues
kubectl-ai "show me the status of all deployments in todo-app namespace"

# Use Kagent for advanced analysis
kagent "analyze the cluster health"
kagent "optimize resource allocation"
kagent "check deployment todo-app health"
```

## Step 7: Access the Application

```bash
# Get Minikube IP
minikube ip

# Access via dashboard
minikube dashboard

# Or set up port forwarding for testing
kubectl port-forward -n todo-app service/frontend-service 3000:3000

# For ingress access, you might need to run:
minikube tunnel  # Run in separate terminal
```

## Step 8: AI-Assisted Operations

```bash
# Scale deployments with kubectl-ai
kubectl-ai "scale the backend to handle more load"
kubectl-ai "deploy the todo frontend with 2 replicas"

# Troubleshoot with kubectl-ai
kubectl-ai "analyze logs from backend deployment"
kubectl-ai "show me resource usage of frontend pods"

# Advanced analysis with Kagent
kagent "generate a performance report for todo-app namespace"
kagent "suggest optimizations for the current deployment"
```

## Step 9: Verify Deployment

```bash
# Check all resources
kubectl get all -n todo-app

# Check ingress
kubectl get ingress -n todo-app

# Check HPA
kubectl get hpa -n todo-app

# Check logs
kubectl logs -f deployment/backend-deployment -n todo-app
kubectl logs -f deployment/frontend-deployment -n todo-app

# Use kubectl-ai for verification
kubectl-ai "verify all services are running in todo-app namespace"
```

## Step 10: Testing the AI Chatbot Functionality

```bash
# Test the application endpoints
kubectl exec -it -n todo-app deployment/frontend-deployment -- curl http://backend-service:8000/health

# Use kubectl-ai to test connectivity
kubectl-ai "test connectivity between frontend and backend services"
```

## Troubleshooting with AI Tools

```bash
# If pods are failing
kubectl-ai "check why the pods are failing"
kubectl-ai "show me the last 100 lines of logs from failed pods"

# If services aren't accessible
kubectl-ai "diagnose why service frontend-service isn't accessible"
kubectl-ai "check ingress configuration for todo-app"

# Performance issues
kubectl-ai "analyze resource usage and suggest optimizations"
kagent "analyze cluster performance and suggest improvements"
```

## Cleanup

```bash
# Uninstall Helm release
helm uninstall todo-app --namespace todo-app

# Or delete namespace
kubectl delete namespace todo-app

# Stop Minikube
minikube stop

# To completely reset Minikube
minikube delete
```

## AI Agent Prompts for Common Tasks

```bash
# Useful kubectl-ai prompts:
kubectl-ai "deploy the todo frontend with 2 replicas"
kubectl-ai "scale the backend to handle more load"
kubectl-ai "check why the pods are failing"
kubectl-ai "show me all resources in todo-app namespace"
kubectl-ai "restart the backend deployment"
kubectl-ai "increase memory limits for frontend deployment"

# Useful Kagent prompts:
kagent "analyze the cluster health"
kagent "optimize resource allocation"
kagent "generate a security audit report"
kagent "analyze deployment patterns and suggest improvements"
```

Your AI Chatbot application should now be running on your local Minikube cluster with AI-assisted deployment and management capabilities!