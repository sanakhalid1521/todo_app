# Vercel Deployment Guide for Todo App

This guide will walk you through deploying your Todo app to Vercel, including both the frontend and backend components.

## Prerequisites

1. Sign up for a [Vercel account](https://vercel.com/)
2. Install the Vercel CLI globally: `npm install -g vercel`
3. Have your Neon Postgres database connection string ready

## Frontend Deployment to Vercel

### Step 1: Navigate to the frontend directory
```bash
cd frontend
```

### Step 2: Set up environment variables in Vercel dashboard
Go to your Vercel dashboard and set these environment variables:
- `NEXT_PUBLIC_API_BASE_URL`: Set to your backend URL (e.g., your deployed backend URL or `http://localhost:8000` for local dev)
- `NEXT_PUBLIC_AUTH_SECRET`: Your 32-character secret key
- `DATABASE_URL`: Your Neon Postgres database connection string
- `JWT_ALGORITHM`: Usually `HS256`
- `JWT_EXPIRATION_DAYS`: Number of days for JWT expiration (e.g., `7`)
- `CORS_ORIGINS`: Your frontend URL (e.g., `https://your-project.vercel.app`)

### Step 3: Deploy the frontend
```bash
vercel --prod
```

## Backend Deployment Options

You have several options for deploying the backend:

### Option 1: Deploy Backend to Vercel Functions (Recommended for small apps)
1. Create a new directory `frontend/api/backend/[...path]/route.ts` to proxy backend requests
2. Or use a service like Railway, Render, or Heroku for the backend

### Option 2: Deploy Backend Separately (Recommended for full features)
Deploy the backend to a service like:
- [Railway](https://railway.app)
- [Render](https://render.com)
- [Heroku](https://heroku.com)
- [AWS EC2/App Runner]
- [Google Cloud Run]

Then update your frontend's `NEXT_PUBLIC_API_BASE_URL` to point to your backend.

## Docker Image Creation

### Building Frontend Docker Image
```bash
cd frontend
docker build -f Dockerfile.vercel -t todo-frontend .
```

### Building Backend Docker Image
```bash
docker build -f Dockerfile.prod -t todo-backend .
```

### Running the containers
```bash
# Start backend first
docker run -d -p 8000:8000 --name todo-backend -e DATABASE_URL="your-neon-db-url" todo-backend

# Then start frontend
docker run -d -p 3000:3000 --name todo-frontend -e NEXT_PUBLIC_API_BASE_URL="http://localhost:8000" todo-frontend
```

## Using the Vercel CLI

### One-time setup
```bash
cd frontend
vercel login
vercel pull --environment=production
```

### Deploy for preview
```bash
vercel
```

### Deploy to production
```bash
vercel --prod
```

## Environment Variables Setup

### In Vercel Dashboard:
1. Go to your project settings in the Vercel dashboard
2. Navigate to "Environment Variables"
3. Add the following variables:

#### For Frontend:
- `NEXT_PUBLIC_API_BASE_URL` - URL of your backend API
- `NEXT_PUBLIC_AUTH_SECRET` - Secret key for authentication

#### For Backend (if deploying separately):
- `DATABASE_URL` - Neon Postgres connection string
- `BETTER_AUTH_SECRET` - Secret key for authentication
- `JWT_ALGORITHM` - Algorithm for JWT (default: HS256)
- `JWT_EXPIRATION_DAYS` - Days for JWT expiration (default: 7)
- `CORS_ORIGINS` - Origins allowed for CORS (comma separated)

## Neon Database Setup

1. Sign up for [Neon](https://neon.tech/)
2. Create a new project
3. Get your connection string from the project dashboard
4. Format: `postgresql://username:password@endpoint.region.neon.tech/dbname?sslmode=require`

## Troubleshooting

### Common Issues:
1. **API calls failing**: Check that `NEXT_PUBLIC_API_BASE_URL` is correctly set
2. **Database connection errors**: Verify your Neon connection string
3. **Authentication not working**: Ensure `BETTER_AUTH_SECRET` is consistent across frontend and backend

### Frontend Build Errors:
- Ensure all dependencies are properly listed in `package.json`
- Check that your `next.config.ts` is properly configured

## Scaling Considerations

For production applications:
- Use a production-ready database (Neon Postgres)
- Implement proper error handling
- Set up monitoring and logging
- Use CDN for static assets
- Implement caching strategies