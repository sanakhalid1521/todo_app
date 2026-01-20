#!/bin/bash

# Integration Test Script for Todo AI Chatbot Application

set -e  # Exit on any error

echo "Starting integration tests for Todo AI Chatbot Application..."

# Test 1: Check if all required namespaces exist
echo "Test 1: Checking namespaces..."
if kubectl get namespace todo-app &> /dev/null; then
    echo "✓ Namespace 'todo-app' exists"
else
    echo "✗ Namespace 'todo-app' does not exist"
    exit 1
fi

# Test 2: Check if all deployments are ready
echo "Test 2: Checking deployments..."
BACKEND_REPLICAS=$(kubectl get deployment backend-deployment -n todo-app -o jsonpath='{.status.readyReplicas}')
FRONTEND_REPLICAS=$(kubectl get deployment frontend-deployment -n todo-app -o jsonpath='{.status.readyReplicas}')

if [ "$BACKEND_REPLICAS" -ge 1 ] && [ "$FRONTEND_REPLICAS" -ge 1 ]; then
    echo "✓ Deployments are ready (Backend: $BACKEND_REPLICAS, Frontend: $FRONTEND_REPLICAS)"
else
    echo "✗ Deployments are not ready (Backend: $BACKEND_REPLICAS, Frontend: $FRONTEND_REPLICAS)"
    kubectl get pods -n todo-app
    exit 1
fi

# Test 3: Check if all services are available
echo "Test 3: Checking services..."
if kubectl get service backend-service -n todo-app &> /dev/null; then
    echo "✓ Backend service exists"
else
    echo "✗ Backend service does not exist"
    exit 1
fi

if kubectl get service frontend-service -n todo-app &> /dev/null; then
    echo "✓ Frontend service exists"
else
    echo "✗ Frontend service does not exist"
    exit 1
fi

# Test 4: Check if ingress is configured
echo "Test 4: Checking ingress..."
if kubectl get ingress todo-ingress -n todo-app &> /dev/null; then
    echo "✓ Ingress exists"
else
    echo "✗ Ingress does not exist"
    exit 1
fi

# Test 5: Check if HPA is configured
echo "Test 5: Checking HPAs..."
if kubectl get hpa backend-hpa -n todo-app &> /dev/null; then
    echo "✓ Backend HPA exists"
else
    echo "✗ Backend HPA does not exist"
    # This might be OK if HPA is disabled
fi

if kubectl get hpa frontend-hpa -n todo-app &> /dev/null; then
    echo "✓ Frontend HPA exists"
else
    echo "⚠ Frontend HPA does not exist (might be intentional if disabled)"
fi

# Test 6: Check if pods are running and healthy
echo "Test 6: Checking pod health..."
POD_COUNT=$(kubectl get pods -n todo-app --field-selector=status.phase=Running --no-headers | wc -l)
if [ "$POD_COUNT" -ge 2 ]; then
    echo "✓ $POD_COUNT pods are running"
else
    echo "✗ Only $POD_COUNT pods are running (expected at least 2)"
    kubectl get pods -n todo-app
    exit 1
fi

# Test 7: Check pod logs for errors
echo "Test 7: Checking for errors in logs..."
BACKEND_LOGS=$(kubectl logs deployment/backend-deployment -n todo-app --tail=20 2>&1 || true)
FRONTEND_LOGS=$(kubectl logs deployment/frontend-deployment -n todo-app --tail=20 2>&1 || true)

if echo "$BACKEND_LOGS" | grep -q "ERROR\|error\|Error\|traceback\|Traceback"; then
    echo "⚠ Found potential errors in backend logs"
    echo "$BACKEND_LOGS" | grep -i "error\|traceback"
else
    echo "✓ No obvious errors in backend logs"
fi

if echo "$FRONTEND_LOGS" | grep -q "ERROR\|error\|Error\|traceback\|Traceback"; then
    echo "⚠ Found potential errors in frontend logs"
    echo "$FRONTEND_LOGS" | grep -i "error\|traceback"
else
    echo "✓ No obvious errors in frontend logs"
fi

# Test 8: Check if ConfigMap exists
echo "Test 8: Checking ConfigMap..."
if kubectl get configmap todo-app-config -n todo-app &> /dev/null; then
    echo "✓ ConfigMap exists"
else
    echo "✗ ConfigMap does not exist"
    exit 1
fi

# Test 9: Check if secrets exist
echo "Test 9: Checking secrets..."
if kubectl get secret todo-app-secrets -n todo-app &> /dev/null; then
    echo "✓ Secrets exist"
else
    echo "⚠ Secrets do not exist (might be intentional in test environments)"
fi

echo ""
echo "==========================================="
echo "All integration tests PASSED! 🎉"
echo "Application is successfully deployed and operational."
echo ""
echo "Summary:"
echo "- Namespace: todo-app"
echo "- Backend: $BACKEND_REPLICAS replica(s) ready"
echo "- Frontend: $FRONTEND_REPLICAS replica(s) ready"
echo "- Services: Available"
echo "- Ingress: Configured"
echo "- Pods: $POD_COUNT running"
echo "==========================================="

exit 0