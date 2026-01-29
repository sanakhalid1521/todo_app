@echo off
REM Minikube Deployment Batch Script for Todo AI Chatbot Application
REM Part of Phase IV: Kubernetes Containerization

echo 🚀 Starting Minikube deployment for Todo AI Chatbot Application...

REM Check prerequisites
echo 🔍 Checking prerequisites...

where minikube >nul 2>&1
if errorlevel 1 (
    echo ❌ minikube is not installed. Please install minikube first.
    exit /b 1
)

where kubectl >nul 2>&1
if errorlevel 1 (
    echo ❌ kubectl is not installed. Please install kubectl first.
    exit /b 1
)

where helm >nul 2>&1
if errorlevel 1 (
    echo ❌ helm is not installed. Please install helm first.
    exit /b 1
)

REM Start Minikube if not already running
minikube status >nul 2>&1
if errorlevel 1 (
    echo 🔄 Starting Minikube...
    minikube start --memory=4096 --cpus=2
) else (
    echo ✅ Minikube is already running
)

REM Enable required addons
echo 🔧 Enabling required Minikube addons...
minikube addons enable ingress
minikube addons enable metrics-server

REM Set Docker environment to Minikube
echo 🐳 Setting Docker environment to Minikube...
call minikube docker-env --shell powershell | powershell

REM Build Docker images
echo 🔨 Building Docker images...
cd ..
docker build -t todo-backend:latest .
docker build -t todo-frontend:latest -f ./frontend/Dockerfile ./frontend
echo ✅ Docker images built successfully

REM Return to k8s/helm directory
cd k8s/helm

REM Create namespace
echo 📦 Creating namespace todo-app...
kubectl create namespace todo-app --dry-run=client -o yaml ^| kubectl apply -f -

REM Prepare secrets (placeholder - in real deployment, replace with actual values)
echo 🔐 Creating placeholder secrets...
set /p DATABASE_URL_B64="Enter Base64-encoded DATABASE_URL: "
set /p OPENAI_API_KEY_B64="Enter Base64-encoded OPENAI_API_KEY: "
set /p AUTH_SECRET_B64="Enter Base64-encoded BETTER_AUTH_SECRET: "

kubectl create secret generic todo-app-secrets ^
  --from-literal=DATABASE_URL="%DATABASE_URL_B64%" ^
  --from-literal=OPENAI_API_KEY="%OPENAI_API_KEY_B64%" ^
  --from-literal=BETTER_AUTH_SECRET="%AUTH_SECRET_B64%" ^
  -n todo-app --dry-run=client -o yaml ^| kubectl apply -f - ^|^| echo "Secrets already exist, continuing..."

REM Install Helm chart
echo 🚢 Installing Helm chart using Minikube-specific values...
helm upgrade --install todo-app . ^
  --namespace todo-app ^
  --values values-minikube.yaml ^
  --set secrets.databaseUrl="%DATABASE_URL_B64%" ^
  --set secrets.openaiApiKey="%OPENAI_API_KEY_B64%" ^
  --set secrets.authSecret="%AUTH_SECRET_B64%" ^
  --debug

REM Wait for deployments to be ready
echo ⏳ Waiting for deployments to be ready...
kubectl wait --for=condition=ready pod -l app=backend -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=frontend -n todo-app --timeout=300s

REM Display deployment status
echo ✅ Deployment completed successfully!
echo.
echo 📋 Deployment status:
kubectl get all -n todo-app

echo.
echo 🌐 To access the application, run:
echo    minikube service frontend-service -n todo-app
echo.
echo 📊 To monitor the application, run:
echo    kubectl get pods,svc,ingress,hpa -n todo-app
echo.
echo 📝 To view logs, run:
echo    kubectl logs -f deployment/backend-deployment -n todo-app
echo    kubectl logs -f deployment/frontend-deployment -n todo-app