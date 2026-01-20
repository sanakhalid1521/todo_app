# Kubernetes Deployment for Todo AI Chatbot Application

This directory contains all Kubernetes manifests and Helm charts for deploying the Todo AI Chatbot application to a Kubernetes cluster.

## Directory Structure

```
k8s/
├── backend-deployment.yaml     # Backend deployment and service
├── frontend-deployment.yaml    # Frontend deployment and service
├── ingress.yaml               # Ingress configuration for external access
├── configmap.yaml             # Application configuration
├── hpa.yaml                   # Horizontal Pod Autoscalers
├── network-policy.yaml        # Network security policies
├── rbac.yaml                  # Role-based access control
├── secrets/                   # Secret templates
│   ├── prod-secrets.yaml
│   └── dev-secrets.yaml
├── helm/                      # Helm chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
├── monitoring/                # Monitoring stack
│   ├── prometheus-config.yaml
│   ├── grafana-deployment.yaml
│   └── service-monitor.yaml
├── DEPLOYMENT_GUIDE.md        # Complete deployment guide
├── integration-test.sh        # Integration test script
└── README.md                  # This file
```

## Quick Start

### Using Helm (Recommended)

1. Create the namespace:
   ```bash
   kubectl create namespace todo-app
   ```

2. Install the application:
   ```bash
   helm install todo-app ./k8s/helm --namespace todo-app \
     --set secrets.databaseUrl="<BASE64_ENCODED_DB_URL>" \
     --set secrets.openaiApiKey="<BASE64_ENCODED_OPENAI_KEY>" \
     --set secrets.authSecret="<BASE64_ENCODED_AUTH_SECRET>"
   ```

### Manual Deployment

Apply all manifests in sequence:

```bash
kubectl apply -f k8s/configmap.yaml -n todo-app
kubectl apply -f k8s/secrets/prod-secrets.yaml -n todo-app
kubectl apply -f k8s/backend-deployment.yaml -n todo-app
kubectl apply -f k8s/frontend-deployment.yaml -n todo-app
kubectl apply -f k8s/ingress.yaml -n todo-app
kubectl apply -f k8s/hpa.yaml -n todo-app
kubectl apply -f k8s/network-policy.yaml -n todo-app
kubectl apply -f k8s/rbac.yaml -n todo-app
```

## Features

- **Auto-scaling**: Horizontal Pod Autoscalers for both frontend and backend
- **Service Discovery**: Internal communication between services
- **Load Balancing**: NGINX Ingress for external access
- **Security**: Network policies and RBAC configurations
- **Observability**: Prometheus and Grafana monitoring stack
- **Configuration Management**: ConfigMaps for application settings
- **Secrets Management**: Secure storage for sensitive data
- **Health Checks**: Liveness and readiness probes

## Configuration

See `k8s/helm/values.yaml` for configurable parameters.

## Monitoring

The monitoring stack includes:
- Prometheus for metrics collection
- Grafana for dashboards and visualization
- ServiceMonitors for application metrics

## Testing

Run integration tests:
```bash
chmod +x k8s/integration-test.sh
./k8s/integration-test.sh
```

## Deployment Guide

For detailed deployment instructions, see [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md).