# Frontend Container Troubleshooting Guide

## Issue Description
The frontend container was not running properly in Kubernetes due to missing health check endpoints.

## Root Cause
1. The Dockerfile contained a HEALTHCHECK instruction looking for `/health` endpoint
2. The Kubernetes deployment had liveness and readiness probes pointing to `/health`
3. The Next.js application did not have a `/health` or `/api/health` endpoint implemented
4. This caused the health checks to fail, resulting in continuous pod restarts

## Solution Applied
1. **Created health endpoint**: Added `/api/health` route in the Next.js application
2. **Updated Dockerfile**: Changed health check from `/health` to `/api/health`
3. **Updated Kubernetes deployment**: Modified liveness/readiness probes to use `/api/health`

## Files Modified
- `frontend/app/api/health/route.ts` - Added health endpoint
- `frontend/Dockerfile` - Updated HEALTHCHECK path
- `k8s/helm/templates/frontend-deployment.yaml` - Updated Kubernetes probes

## Health Endpoint Details
The health endpoint at `/api/health` returns:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-29T10:30:00.000Z",
  "uptime": 123.45,
  "checks": {
    "frontend": "ok",
    "backend_connectivity": "configured"
  }
}
```

## Verification Steps
After deployment, verify the frontend is running:

```bash
# Check pod status
kubectl get pods -n todo-app

# Check pod logs
kubectl logs -f deployment/frontend-deployment -n todo-app

# Test health endpoint manually (if pod is accessible)
kubectl exec -it <frontend-pod-name> -n todo-app -- wget --quiet --output-document=- http://localhost:3000/api/health

# Check service connectivity
kubectl port-forward svc/frontend-service 3000:3000 -n todo-app
curl http://localhost:3000/api/health
```

## Expected Results
- Frontend pods should show `Running` status
- No continuous restarts in the pod status
- Health checks should pass consistently
- Application should be accessible through the service/ingress

## Additional Notes
- The backend service already had proper health checks at `/health`
- The frontend uses Next.js App Router, so API routes go under `/api/*`
- Environment variables like `NEXT_PUBLIC_API_BASE_URL` are still properly configured
- CORS settings remain unchanged