@echo off
REM Batch script to configure Neon database settings on Windows

echo Setting up Neon Database Configuration...

REM Check if .env file exists
if not exist ".env" (
    echo Creating .env file...
    echo BETTER_AUTH_SECRET=%%RANDOM%%%%RANDOM%%your-very-secure-32-character-secret-key-here-12345 > .env
    echo OPENAI_API_KEY=your-openai-api-key-here >> .env
    echo DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require >> .env
    echo .env file created with default values.
) else (
    echo .env file exists, checking configuration...
    REM Use PowerShell to update the DATABASE_URL if it contains sqlite
    powershell -Command "(gc .env) -replace 'DATABASE_URL=sqlite.*', 'DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require' | Out-File -encoding UTF8 .env.tmp"
    move /Y .env.tmp .env >nul
    echo DATABASE_URL updated to use Neon.
)

REM Create development docker-compose with Neon configuration
echo version: '3.8' > docker-compose.dev-neon.yml
echo. >> docker-compose.dev-neon.yml
echo services: >> docker-compose.dev-neon.yml
echo   # Backend Server with Neon database >> docker-compose.dev-neon.yml
echo   backend: >> docker-compose.dev-neon.yml
echo     build: >> docker-compose.dev-neon.yml
echo       context: ./backend >> docker-compose.dev-neon.yml
echo       dockerfile: Dockerfile.dev >> docker-compose.dev-neon.yml
echo     container_name: todo-app-backend-neon >> docker-compose.dev-neon.yml
echo     platform: linux/amd64 >> docker-compose.dev-neon.yml
echo     ports: >> docker-compose.dev-neon.yml
echo       - "8000:8000" >> docker-compose.dev-neon.yml
echo     environment: >> docker-compose.dev-neon.yml
echo       DATABASE_URL: ^%DATABASE_URL^% ^|^| postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require >> docker-compose.dev-neon.yml
echo       BETTER_AUTH_SECRET: ^%BETTER_AUTH_SECRET^% ^|^| your-32-character-secret-key-here >> docker-compose.dev-neon.yml
echo       JWT_ALGORITHM: HS256 >> docker-compose.dev-neon.yml
echo       JWT_EXPIRATION_DAYS: 7 >> docker-compose.dev-neon.yml
echo       CORS_ORIGINS: http://localhost:3000,http://frontend:3000 >> docker-compose.dev-neon.yml
echo       OPENAI_API_KEY: ^%OPENAI_API_KEY^% ^|^| your-openai-key-here >> docker-compose.dev-neon.yml
echo       ENVIRONMENT: development >> docker-compose.dev-neon.yml
echo     volumes: >> docker-compose.dev-neon.yml
echo       # Bind mount for live code reloading >> docker-compose.dev-neon.yml
echo       - ./backend:/app >> docker-compose.dev-neon.yml
echo       - /app/.venv  # Exclude virtual environment from sync >> docker-compose.dev-neon.yml
echo     networks: >> docker-compose.dev-neon.yml
echo       - todo-network >> docker-compose.dev-neon.yml
echo     command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "info"] >> docker-compose.dev-neon.yml
echo     healthcheck: >> docker-compose.dev-neon.yml
echo       test: ["CMD", "curl", "-f", "http://localhost:8000/health"] >> docker-compose.dev-neon.yml
echo       interval: 30s >> docker-compose.dev-neon.yml
echo       timeout: 10s >> docker-compose.dev-neon.yml
echo       retries: 3 >> docker-compose.dev-neon.yml
echo       start_period: 40s >> docker-compose.dev-neon.yml
echo. >> docker-compose.dev-neon.yml
echo   # Frontend Server >> docker-compose.dev-neon.yml
echo   frontend: >> docker-compose.dev-neon.yml
echo     build: >> docker-compose.dev-neon.yml
echo       context: ./frontend >> docker-compose.dev-neon.yml
echo       dockerfile: Dockerfile.dev >> docker-compose.dev-neon.yml
echo     container_name: todo-app-frontend-neon >> docker-compose.dev-neon.yml
echo     platform: linux/amd64 >> docker-compose.dev-neon.yml
echo     ports: >> docker-compose.dev-neon.yml
echo       - "3000:3000" >> docker-compose.dev-neon.yml
echo     environment: >> docker-compose.dev-neon.yml
echo       - NEXT_PUBLIC_API_BASE_URL=http://localhost:8000 >> docker-compose.dev-neon.yml
echo       - NEXT_PUBLIC_AUTH_SECRET=^%^BETTER_AUTH_SECRET^%^ ^|^| your-32-character-secret-key-here >> docker-compose.dev-neon.yml
echo       - NODE_ENV=development >> docker-compose.dev-neon.yml
echo     depends_on: >> docker-compose.dev-neon.yml
echo       backend: >> docker-compose.dev-neon.yml
echo         condition: service_healthy >> docker-compose.dev-neon.yml
echo     networks: >> docker-compose.dev-neon.yml
echo       - todo-network >> docker-compose.dev-neon.yml
echo     volumes: >> docker-compose.dev-neon.yml
echo       # Bind mount for live code reloading >> docker-compose.dev-neon.yml
echo       - ./frontend:/app >> docker-compose.dev-neon.yml
echo       - /app/node_modules  # Exclude node_modules from sync >> docker-compose.dev-neon.yml
echo     healthcheck: >> docker-compose.dev-neon.yml
echo       test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000"] >> docker-compose.dev-neon.yml
echo       interval: 30s >> docker-compose.dev-neon.yml
echo       timeout: 10s >> docker-compose.dev-neon.yml
echo       retries: 3 >> docker-compose.dev-neon.yml
echo       start_period: 40s >> docker-compose.dev-neon.yml
echo. >> docker-compose.dev-neon.yml
echo volumes: >> docker-compose.dev-neon.yml
echo   todo_db_volume: >> docker-compose.dev-neon.yml
echo. >> docker-compose.dev-neon.yml
echo networks: >> docker-compose.dev-neon.yml
echo   todo-network: >> docker-compose.dev-neon.yml
echo     driver: bridge >> docker-compose.dev-neon.yml

echo Created docker-compose.dev-neon.yml with Neon configuration.

echo Setup complete! Please:
echo 1. Update the .env file with your actual Neon database URL
echo 2. Run: docker-compose -f docker-compose.dev-neon.yml up --build
echo 3. Or for Kubernetes: helm install todo-app ./k8s/helm -f k8s/helm/values.dev.yaml