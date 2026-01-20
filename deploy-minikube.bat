@echo off
setlocal enabledelayedexpansion

echo ================================================
echo  Todo AI Chatbot - Minikube Deployment Script
echo ================================================
echo.

REM Check if Minikube is installed
where minikube >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Minikube is not installed or not in PATH
    echo Please install Minikube first
    pause
    exit /b 1
)

REM Check if kubectl is installed
where kubectl >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: kubectl is not installed or not in PATH
    echo Please install kubectl first
    pause
    exit /b 1
)

REM Check if Helm is installed
where helm >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Helm is not installed or not in PATH
    echo Please install Helm first
    pause
    exit /b 1
)

echo 1. Starting Minikube...
minikube start --cpus=4 --memory=8192 --disk-size=40g
if %errorlevel% neq 0 (
    echo ERROR: Failed to start Minikube
    pause
    exit /b 1
)

echo.
echo 2. Enabling required addons...
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard

echo.
echo 3. Setting Docker environment to Minikube...
call minikube docker-env | Invoke-Expression

echo.
echo 4. Building Docker images...
cd backend
docker build -t todo-backend:latest .
if %errorlevel% neq 0 (
    echo ERROR: Failed to build backend image
    pause
    exit /b 1
)
cd ..

cd frontend
docker build -t todo-frontend:latest .
if %errorlevel% neq 0 (
    echo ERROR: Failed to build frontend image
    pause
    exit /b 1
)
cd ..

echo.
echo 5. Creating namespace...
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

echo.
echo 6. Applying Kubernetes configurations...
kubectl apply -f k8s/configmap.yaml -n todo-app
kubectl apply -f k8s/backend-deployment.yaml -n todo-app
kubectl apply -f k8s/frontend-deployment.yaml -n todo-app
kubectl apply -f k8s/ingress.yaml -n todo-app
kubectl apply -f k8s/hpa.yaml -n todo-app
kubectl apply -f k8s/network-policy.yaml -n todo-app
kubectl apply -f k8s/rbac.yaml -n todo-app

echo.
echo 7. Waiting for deployments to be ready...
kubectl wait --for=condition=ready pod -l app=backend -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=frontend -n todo-app --timeout=300s

echo.
echo 8. Verifying deployment status...
kubectl get pods -n todo-app
kubectl get services -n todo-app
kubectl get ingress -n todo-app

echo.
echo ================================================
echo  Deployment completed successfully!
echo.
echo  To access the application:
echo  - Run: minikube tunnel (in a separate terminal)
echo  - Access: http://todo-app.local
echo.
echo  To check status: kubectl get pods -n todo-app
echo  To view logs: kubectl logs -f deployment/backend-deployment -n todo-app
echo ================================================

pause