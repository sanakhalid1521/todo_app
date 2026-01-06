# Deployment Guide

This guide provides instructions for deploying the full-stack todo application to various platforms.

## Frontend Deployment (Vercel)

### Prerequisites
- A Vercel account
- The Vercel CLI installed (`npm install -g vercel`)

### Steps
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Deploy to Vercel:
   ```bash
   vercel
   ```

4. Follow the prompts to configure your project:
   - Set the build command to `npm run build`
   - Set the output directory to `out` (or leave default)
   - Set the development command (optional)

5. Add environment variables in the Vercel dashboard:
   - `NEXT_PUBLIC_API_URL`: Your backend API URL (e.g., `https://your-backend-app.vercel.app`)

### Environment Variables
Make sure to set the following environment variable in your Vercel project settings:
- `NEXT_PUBLIC_API_URL`: The URL of your deployed backend API

## Backend Deployment (Heroku/Railway)

### Deploying to Railway

1. Create a Railway account and install the Railway CLI
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```
3. Create a new Railway project:
   ```bash
   railway login
   railway init
   ```
4. Link your project:
   ```bash
   railway link <project-id>
   ```
5. Set environment variables:
   ```bash
   railway vars set DATABASE_URL=your-postgres-url
   railway vars set JWT_SECRET_KEY=your-jwt-secret
   # Add other required environment variables
   ```
6. Deploy:
   ```bash
   railway up
   ```

### Deploying to Heroku

1. Create a Heroku account and install the Heroku CLI
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```
3. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```
4. Set environment variables:
   ```bash
   heroku config:set DATABASE_URL=your-postgres-url
   heroku config:set JWT_SECRET_KEY=your-jwt-secret
   # Add other required environment variables
   ```
5. Deploy:
   ```bash
   git push heroku main
   ```

## Database Setup

The application uses PostgreSQL with Neon for production. When deploying:

1. Create a Neon PostgreSQL database
2. Set the `DATABASE_URL` environment variable to your database connection string
3. The application will automatically create the necessary tables on startup

## Configuration Notes

### CORS Settings
Make sure your backend CORS settings include your frontend URL:
- For local development: `http://localhost:3000`
- For Vercel deployments: `https://*.vercel.app`

### Authentication
The application uses Better Auth for authentication. Make sure to:
- Set the `BETTER_AUTH_SECRET` environment variable
- Configure the correct callback URLs for your deployment
- Set up email verification if required

## Troubleshooting

### Frontend Deployment Issues
- Ensure `NEXT_PUBLIC_API_URL` is correctly set
- Check that the backend API is accessible from your frontend domain
- Verify that CORS headers are properly configured

### Backend Deployment Issues
- Confirm that the database connection string is correct
- Check that all required environment variables are set
- Verify that the application can create tables in the database

### Common Issues
- 500 errors: Check logs for database connection issues
- 403 errors: Verify authentication tokens and headers
- CORS errors: Ensure frontend domain is allowed in backend settings

## Post-Deployment Steps

1. Test all API endpoints
2. Verify authentication flow
3. Confirm task creation, reading, updating, and deletion work
4. Test the chatbot functionality if deployed
5. Monitor application logs for any errors