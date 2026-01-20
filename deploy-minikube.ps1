Write-Host "=========================================" -ForegroundColor Green
Write-Host "  Todo AI Chatbot - Minikube Deployment Script" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Check if Minikube is installed
if (!(Get-Command minikube -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Minikube is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Minikube first" -ForegroundColor Red
    Read-Host "Press any key to exit"
    exit 1
}

# Check if kubectl is installed
if (!(Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: kubectl is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install kubectl first" -ForegroundColor Red
    Read-Host "Press any key to exit"
    exit 1
}

# Check if Helm is installed
if (!(Get-Command helm -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Helm is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Helm first" -ForegroundColor Red
    Read-Host "Press any key to exit"
    exit 1
}

Write-Host "`n1. Starting Minikube..." -ForegroundColor Yellow
minikube start --cpus=4 --memory=8192 --disk-size=40g
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to start Minikube" -ForegroundColor Red
    Read-Host "Press any key to exit"
    exit 1
}

Write-Host "`n2. Enabling required addons..." -ForegroundColor Yellow
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard

Write-Host "`n3. Setting Docker environment to Minikube..." -ForegroundColor Yellow
minikube docker-env | Invoke-Expression

Write-Host "`n4. Building Docker images..." -ForegroundColor Yellow
Set-Location backend
docker build -t todo-backend:latest .
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to build backend image" -ForegroundColor Red
    Read-Host "Press any key to exit"
    exit 1
}
Set-Location ..

Set-Location frontend
docker build -t todo-frontend:latest .
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to build frontend image" -ForegroundColor Red
    Read-Host "Press any key to exit"
    exit 1
}
Set-Location ..

Write-Host "`n5. Creating namespace..." -ForegroundColor Yellow
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

Write-Host "`n6. Applying Kubernetes configurations..." -ForegroundColor Yellow
kubectl apply -f k8s/configmap.yaml -n todo-app
kubectl apply -f k8s/backend-deployment.yaml -n todo-app
kubectl apply -f k8s/frontend-deployment.yaml -n todo-app
kubectl apply -f k8s/ingress.yaml -n todo-app
kubectl apply -f k8s/hpa.yaml -n todo-app
kubectl apply -f k8s/network-policy.yaml -n todo-app
kubectl apply -f k8s/rbac.yaml -n todo-app

Write-Host "`n7. Waiting for deployments to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=backend -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=frontend -n todo-app --timeout=300s

Write-Host "`n8. Verifying deployment status..." -ForegroundColor Yellow
kubectl get pods -n todo-app
kubectl get services -n todo-app
kubectl get ingress -n todo-app

Write-Host "`n=========================================" -ForegroundColor Green
Write-Host "Deployment completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To access the application:" -ForegroundColor Cyan
Write-Host "  - Run: minikube tunnel (in a separate terminal)" -ForegroundColor Cyan
Write-Host "  - Access: http://todo-app.local" -ForegroundColor Cyan
Write-Host ""
Write-Host "To check status: kubectl get pods -n todo-app" -ForegroundColor Cyan
Write-Host "To view logs: kubectl logs -f deployment/backend-deployment -n todo-app" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Green

Read-Host "`nPress any key to exit"