# Deploying AI-Powered Todo Chatbot to Hugging Face Spaces

This guide provides step-by-step instructions for deploying the AI-Powered Todo Chatbot application to Hugging Face Spaces.

## Prerequisites

1. **Hugging Face Account**: Create an account at [huggingface.co](https://huggingface.co)
2. **OpenAI API Key**: Obtain an API key from [OpenAI](https://platform.openai.com/api-keys)
3. **Git Repository**: The application code should be hosted on Hugging Face Hub or GitHub

## Deployment Options

### Option 1: Direct Deployment from Hugging Face Hub (Recommended)

1. **Fork or Create Repository**:
   - Create a new repository on Hugging Face Hub
   - Or fork an existing repository containing the AI Todo Chatbot code

2. **Add Required Files**:
   Ensure your repository contains:
   - `app.py` - Main application entry point
   - `Dockerfile.hf` - Docker configuration for Hugging Face
   - `app.json` - Space configuration
   - `README.hf.md` - Space description
   - `requirements.txt` - Python dependencies

3. **Create the Space**:
   - Go to your Hugging Face profile
   - Click "New Space"
   - Choose "Docker" as the SDK
   - Select "GPU" or "CPU" based on your needs (CPU is sufficient for this app)
   - Link your repository

4. **Configure Secrets**:
   - Go to your Space settings
   - Add the required secrets:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `DATABASE_URL`: Database connection string (optional)

### Option 2: Using Git Operations

1. **Clone Your Hugging Face Repository**:
   ```bash
   git clone https://huggingface.co/spaces/your-username/your-space-name
   ```

2. **Copy Required Files**:
   ```bash
   cp Dockerfile.hf Dockerfile
   cp app.json ./  # Space configuration
   cp README.hf.md README.md
   cp .env.example.hf .env
   ```

3. **Commit and Push**:
   ```bash
   git add .
   git commit -m "Add Hugging Face Space configuration"
   git push origin main
   ```

## Required Environment Variables

The following environment variables need to be configured in your Space settings:

### Secrets (Required)
- `OPENAI_API_KEY`: Your OpenAI API key for AI functionality

### Environment Variables (Optional)
- `DATABASE_URL`: PostgreSQL database URL (defaults to SQLite if not provided)
- `NEXT_PUBLIC_API_URL`: Backend API URL (usually defaults to the space URL)

## Architecture Overview

The deployed application includes:

- **FastAPI Backend**: Handles API requests and business logic
- **AI Integration**: OpenAI-powered chatbot for natural language task management
- **Database Layer**: SQLModel with PostgreSQL for persistent storage
- **MCP Tools**: Model Context Protocol for secure tool integration

## Customization

You can customize the Space by modifying:

- `Dockerfile.hf`: Change dependencies or build process
- `app.json`: Update required secrets and environment variables
- `README.hf.md`: Customize the space description and instructions

## Troubleshooting

### Common Issues

1. **Application Won't Start**:
   - Check the Space logs in the "Logs" tab
   - Verify all required secrets are set
   - Ensure the port is correctly configured (should use PORT environment variable)

2. **AI Features Not Working**:
   - Verify OPENAI_API_KEY is correctly set
   - Check OpenAI API usage limits
   - Confirm internet connectivity for API calls

3. **Database Issues**:
   - For production, use a proper PostgreSQL database
   - SQLite may have limitations in the Space environment

### Monitoring

- Check the Space logs regularly for errors
- Monitor API usage if using OpenAI
- Verify that all endpoints are accessible

## Scaling and Performance

The application is designed to scale with Hugging Face Spaces:
- CPU instances are suitable for single-user or light usage
- For higher traffic, consider upgrading to GPU or Pro spaces
- The application uses async database operations for better performance

## Security Considerations

- API keys are stored securely as Space secrets
- The application implements proper authentication
- All user data is isolated per user

## Updating the Deployment

To update your deployed Space:

1. Make changes to your repository
2. Commit and push changes:
   ```bash
   git add .
   git commit -m "Update application"
   git push origin main
   ```
3. The Space will automatically rebuild and redeploy

## Support

For issues with the application itself, refer to the project documentation.
For Hugging Face Spaces platform issues, check the Hugging Face documentation and community forums.