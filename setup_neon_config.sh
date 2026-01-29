#!/bin/bash
# Script to configure Neon database settings

echo "Setting up Neon Database Configuration..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOF
BETTER_AUTH_SECRET=$(openssl rand -hex 16)your-very-secure-32-character-secret-key-here-12345
OPENAI_API_KEY=your-openai-api-key-here
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
EOF
    echo ".env file created with default values."
else
    echo ".env file exists, checking configuration..."
    # Check if DATABASE_URL is set to Neon
    if grep -q "sqlite" .env; then
        echo "Updating DATABASE_URL to use Neon..."
        sed -i.bak 's|DATABASE_URL=.*|DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require|' .env
        echo "DATABASE_URL updated to use Neon."
    fi
fi

# Encode secrets for Kubernetes
echo "Encoding secrets for Kubernetes..."
NEON_DB_B64=$(echo -n "postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require" | base64 -w 0)
OPENAI_KEY_B64=$(echo -n "your-openai-api-key-here" | base64 -w 0)
AUTH_SECRET_B64=$(echo -n "$(openssl rand -hex 16)your-very-secure-32-character-secret-key-here-12345" | base64 -w 0)

echo "Encoded secrets generated."

# Update the secrets in values.dev.yaml
sed -i.bak "s|databaseUrl: \"\"|databaseUrl: \"$NEON_DB_B64\"|" k8s/helm/values.dev.yaml
sed -i.bak "s|openaiApiKey: \"\"|openaiApiKey: \"$OPENAI_KEY_B64\"|" k8s/helm/values.dev.yaml
sed -i.bak "s|authSecret: \"\"|authSecret: \"$AUTH_SECRET_B64\"|" k8s/helm/values.dev.yaml

echo "Kubernetes development values updated with encoded secrets."

# Create/update development docker-compose with Neon configuration
cat > docker-compose.dev-neon.yml << EOF
version: '3.8'

services:
  # Backend Server with Neon database
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    container_name: todo-app-backend-neon
    platform: linux/amd64
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: \${DATABASE_URL:-postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require}
      BETTER_AUTH_SECRET: \${BETTER_AUTH_SECRET:-your-32-character-secret-key-here}
      JWT_ALGORITHM: HS256
      JWT_EXPIRATION_DAYS: 7
      CORS_ORIGINS: http://localhost:3000,http://frontend:3000
      OPENAI_API_KEY: \${OPENAI_API_KEY:-your-openai-key-here}
      ENVIRONMENT: development
    volumes:
      # Bind mount for live code reloading
      - ./backend:/app
      - /app/.venv  # Exclude virtual environment from sync
    networks:
      - todo-network
    command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "info"]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Frontend Server
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    container_name: todo-app-frontend-neon
    platform: linux/amd64
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
      - NEXT_PUBLIC_AUTH_SECRET=\${BETTER_AUTH_SECRET:-your-32-character-secret-key-here}
      - NODE_ENV=development
    depends_on:
      backend:
        condition: service_healthy
    networks:
      - todo-network
    volumes:
      # Bind mount for live code reloading
      - ./frontend:/app
      - /app/node_modules  # Exclude node_modules from sync
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

volumes:
  todo_db_volume:

networks:
  todo-network:
    driver: bridge
EOF

echo "Created docker-compose.dev-neon.yml with Neon configuration."

echo "Setup complete! Please:"
echo "1. Update the .env file with your actual Neon database URL"
echo "2. Update the values.dev.yaml with your actual encoded secrets"
echo "3. Run: docker-compose -f docker-compose.dev-neon.yml up --build"
echo "4. Or for Kubernetes: helm install todo-app ./k8s/helm -f k8s/helm/values.dev.yaml"