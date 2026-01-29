# Phase IV: Local Kubernetes Deployment

This document outlines the implementation of Phase IV of the Todo AI Chatbot application: Local Kubernetes Deployment using Minikube, Helm Charts, and related tools.

## Overview

Phase IV focuses on containerizing the Todo AI Chatbot application and deploying it on a local Kubernetes cluster using Minikube. This phase implements cloud-native deployment practices with container orchestration, automated scaling, and infrastructure as code.

## Architecture

The deployed system consists of:

- **Frontend**: Next.js application deployed as a Kubernetes Deployment
- **Backend**: FastAPI application deployed as a Kubernetes Deployment
- **Database**: External PostgreSQL database (Neon Serverless)
- **Services**: Internal communication via ClusterIP services
- **Ingress**: External access via NGINX Ingress Controller
- **Autoscaling**: Horizontal Pod Autoscalers for dynamic scaling
- **Monitoring**: Prometheus and Grafana for observability

## Components

### Containerization
- Multi-stage Dockerfiles for optimized builds
- Backend: Python 3.10-slim with dependency caching
- Frontend: Node 20-alpine with production-optimized build
- Health checks implemented for both services

### Kubernetes Resources
- Namespaces for resource isolation
- Deployments for application management
- Services for internal communication
- ConfigMaps for configuration
- Secrets for sensitive data
- Network Policies for security
- RBAC configurations for access control
- Horizontal Pod Autoscalers for scaling

### Helm Charts
- Parameterized deployment configurations
- Environment-specific values files
- Template-based resource generation
- Easy deployment and upgrades

## Deployment Options

### 1. Minikube Deployment (Recommended for Development)

#### Prerequisites
- Minikube v1.20+
- kubectl
- Helm 3.x
- Docker Desktop with Gordon (optional)

#### Quick Start
```bash
# Start Minikube
minikube start --memory=4096 --cpus=2
minikube addons enable ingress

# Build and deploy using the helper script
cd k8s
./minikube-deploy.sh  # On Linux/Mac
# OR
minikube-deploy.bat   # On Windows
```

#### Manual Deployment
```bash
# Set up Minikube environment
eval $(minikube docker-env)  # Linux/Mac
# OR
minikube docker-env --shell powershell | powershell  # Windows

# Build images
docker build -t todo-backend:latest .
docker build -t todo-frontend:latest -f ./frontend/Dockerfile ./frontend

# Deploy with Helm
cd k8s/helm
helm install todo-app . \
  --namespace todo-app \
  --values values-minikube.yaml \
  --set secrets.databaseUrl="<base64-db-url>" \
  --set secrets.openaiApiKey="<base64-openai-key>" \
  --set secrets.authSecret="<base64-auth-secret>"
```

### 2. AI-Assisted Deployment

Using kubectl-ai and Kagent for intelligent operations:

```bash
# Deploy with AI assistance
kubectl-ai "deploy the todo frontend with 2 replicas in todo-app namespace"
kubectl-ai "configure ingress for the frontend service"
kubectl-ai "check why pods are failing"

# Analyze cluster with Kagent
kagent "analyze the cluster health"
kagent "optimize resource allocation for the todo-app"
```

### 3. Standard Kubernetes Deployment

For deployment to any Kubernetes cluster:

```bash
# Create namespace
kubectl create namespace todo-app

# Apply all manifests
kubectl apply -f k8s/configmap.yaml -n todo-app
kubectl apply -f k8s/secrets/prod-secrets.yaml -n todo-app
kubectl apply -f k8s/backend-deployment.yaml -n todo-app
kubectl apply -f k8s/frontend-deployment.yaml -n todo-app
kubectl apply -f k8s/ingress.yaml -n todo-app
kubectl apply -f k8s/hpa.yaml -n todo-app
kubectl apply -f k8s/network-policy.yaml -n todo-app
kubectl apply -f k8s/rbac.yaml -n todo-app
```

## Configuration

### Environment Variables

#### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: API key for OpenAI integration
- `BETTER_AUTH_SECRET`: Authentication secret
- `CORS_ORIGINS`: Allowed origins for CORS

#### Frontend
- `NEXT_PUBLIC_API_BASE_URL`: Backend API URL
- `NEXT_PUBLIC_AUTH_SECRET`: Auth secret for frontend

### Secrets Management
Sensitive data is stored in Kubernetes Secrets and mounted as environment variables. The Helm chart includes templates for secret creation.

## Scaling

### Manual Scaling
```bash
kubectl scale deployment backend-deployment --replicas=3 -n todo-app
kubectl scale deployment frontend-deployment --replicas=3 -n todo-app
```

### Auto Scaling
Horizontal Pod Autoscalers are configured based on CPU utilization:
- Backend: Scales between 1-10 replicas
- Frontend: Scales between 1-5 replicas

## Monitoring and Observability

### Built-in Probes
- Liveness probes to detect deadlocks
- Readiness probes to control traffic routing
- Startup probes for slow-starting containers

### Metrics Collection
- Prometheus for metrics collection
- ServiceMonitors for application metrics
- Grafana for dashboard visualization

### Health Checks
- `/health` endpoint on both frontend and backend
- Kubernetes native health checking

## Security

### Network Security
- Network policies restricting traffic between services
- TLS termination at ingress layer
- RBAC for access control

### Secrets Management
- Kubernetes Secrets for sensitive data
- Base64 encoding for secret values
- No hardcoded credentials in manifests

## AIOps Integration

### Docker AI Agent (Gordon)
For intelligent Docker operations:
```bash
docker ai "What can you do?"
docker ai "Build an optimized Docker image for the backend"
```

### kubectl-ai and Kagent
For AI-assisted Kubernetes operations:
```bash
kubectl-ai "deploy the todo frontend with 2 replicas"
kagent "analyze the cluster health"
```

## Troubleshooting

### Common Issues
1. **Images not found**: Ensure Docker images are built in Minikube's context
2. **Services not accessible**: Check ingress controller status
3. **Database connection errors**: Verify database URL in secrets
4. **API key errors**: Confirm OpenAI API key is properly configured

### Debugging Commands
```bash
# Check pod status
kubectl get pods -n todo-app

# View logs
kubectl logs -f deployment/backend-deployment -n todo-app

# Describe resources
kubectl describe pod <pod-name> -n todo-app

# Port forward for direct access
kubectl port-forward service/backend-service 8000:8000 -n todo-app
```

## Testing

Integration tests are available to verify deployment:
```bash
chmod +x k8s/integration-test.sh
./k8s/integration-test.sh
```

## Cleanup

To remove the deployment:
```bash
# Using Helm
helm uninstall todo-app --namespace todo-app

# Or delete namespace
kubectl delete namespace todo-app
```

## Next Steps (Phase V)

With Phase IV complete, the foundation is set for:
- Advanced cloud deployment (AWS/GCP/Azure)
- CI/CD pipeline implementation
- Advanced monitoring and alerting
- Performance optimization
- Security hardening

## Conclusion

Phase IV successfully implements Kubernetes containerization for the Todo AI Chatbot application, providing a scalable, observable, and maintainable deployment architecture. The solution leverages modern cloud-native practices while maintaining flexibility for future enhancements.