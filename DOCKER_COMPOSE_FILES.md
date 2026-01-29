# Docker Compose Files Guide

This project contains multiple Docker Compose files for different environments and purposes. Here's a guide to understand which file to use:

## Active/Recommended Files

### 1. `docker-compose.yml` - Production-like Setup
- Purpose: Main configuration for production-like deployment
- Contains: Backend (FastAPI) and Frontend (Next.js) services
- Database: SQLite (via environment variable)
- Ports: Backend on 8000, Frontend on 3000
- Best for: Testing production-like setup

### 2. `docker-compose.dev.yml` - Development Setup (Primary)
- Purpose: Primary development environment with hot-reloading
- Contains: Backend, Frontend, and PostgreSQL database services
- Features:
  - Live code reloading with bind mounts
  - .env file mounting
  - Health checks
  - Proper dependency ordering
- Ports: Backend on 8000, Frontend on 3001, DB on 5432
- Best for: Active development

### 3. `docker-compose-run.yml` - Current Working Setup
- Purpose: Currently running setup with port adjustments
- Contains: Pre-built images with custom port mapping
- Features:
  - Uses existing built images
  - Avoids port conflicts (DB on 5433, Backend on 8001, Frontend on 3001)
  - Bind mounts for live reloading
- Best for: Quick startup of current working environment

### 4. `docker-compose.dev-neon.yml` - Neon Database Setup
- Purpose: Development with Neon PostgreSQL database
- Contains: Backend and Frontend services
- Database: Connects to Neon cloud PostgreSQL
- Best for: Development with cloud database

### 5. `docker-compose.prod.yml` - Production Setup
- Purpose: Production-ready configuration
- Contains: Optimized settings for production
- Features:
  - Production Dockerfiles
  - Restart policies
  - Production environment variables
- Best for: Production deployments

## Files Removed

The following files were removed as they were duplicates or less optimal:
- `docker-compose-enhanced.yml` - Redundant copy of working config
- `docker-compose.fixed.yml` - Older version with limited features

## Recommended Usage

For **active development**: Use `docker-compose.dev.yml`
```bash
docker-compose -f docker-compose.dev.yml up -d
```

For **quick startup** with existing images: Use `docker-compose-run.yml`
```bash
docker-compose -f docker-compose-run.yml up -d
```

For **production testing**: Use `docker-compose.yml` or `docker-compose.prod.yml`
```bash
docker-compose -f docker-compose.yml up -d
```

For **Neon database development**: Use `docker-compose.dev-neon.yml`
```bash
docker-compose -f docker-compose.dev-neon.yml up -d
```