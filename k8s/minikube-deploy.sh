#!/bin/bash

# Minikube Deployment Script for Todo AI Chatbot Application
# Part of Phase IV: Kubernetes Containerization

set -e  # Exit on any error

echo "🚀 Starting Minikube deployment for Todo AI Chatbot Application..."

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command -v minikube &> /dev/null; then
    echo "❌ minikube is not installed. Please install minikube first."
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo "❌ helm is not installed. Please install helm first."
    exit 1
fi

# Start Minikube if not already running
if ! minikube status &> /dev/null; then
    echo "🔄 Starting Minikube..."
    minikube start --memory=4096 --cpus=2
else
    echo "✅ Minikube is already running"
fi

# Enable required addons
echo "🔧 Enabling required Minikube addons..."
minikube addons enable ingress
minikube addons enable metrics-server

# Set Docker environment to Minikube
echo "🐳 Setting Docker environment to Minikube..."
eval $(minikube docker-env)

# Build Docker images
echo "🔨 Building Docker images..."
cd ..
docker build -t todo-backend:latest .
docker build -t todo-frontend:latest -f ./frontend/Dockerfile ./frontend
echo "✅ Docker images built successfully"

# Return to k8s/helm directory
cd k8s/helm

# Create namespace
echo "📦 Creating namespace todo-app..."
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

# Prepare secrets (placeholder - in real deployment, replace with actual values)
echo "🔐 Creating placeholder secrets..."
read -p "Enter Base64-encoded DATABASE_URL: " DATABASE_URL_B64
read -p "Enter Base64-encoded OPENAI_API_KEY: " OPENAI_API_KEY_B64
read -s -p "Enter Base64-encoded BETTER_AUTH_SECRET: " AUTH_SECRET_B64
echo

kubectl create secret generic todo-app-secrets \
  --from-literal=DATABASE_URL="$DATABASE_URL_B64" \
  --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY_B64" \
  --from-literal=BETTER_AUTH_SECRET="$AUTH_SECRET_B64" \
  -n todo-app --dry-run=client -o yaml | kubectl apply -f - || echo "Secrets already exist, continuing..."

# Install Helm chart
echo "🚢 Installing Helm chart using Minikube-specific values..."
helm upgrade --install todo-app . \
  --namespace todo-app \
  --values values-minikube.yaml \
  --set secrets.databaseUrl="$DATABASE_URL_B64" \
  --set secrets.openaiApiKey="$OPENAI_API_KEY_B64" \
  --set secrets.authSecret="$AUTH_SECRET_B64" \
  --debug

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app=backend -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=frontend -n todo-app --timeout=300s

# Display deployment status
echo "✅ Deployment completed successfully!"
echo ""
echo "📋 Deployment status:"
kubectl get all -n todo-app

echo ""
echo "🌐 To access the application, run:"
echo "   minikube service frontend-service -n todo-app"
echo ""
echo "📊 To monitor the application, run:"
echo "   kubectl get pods,svc,ingress,hpa -n todo-app"
echo ""
echo "📝 To view logs, run:"
echo "   kubectl logs -f deployment/backend-deployment -n todo-app"
echo "   kubectl logs -f deployment/frontend-deployment -n todo-app"