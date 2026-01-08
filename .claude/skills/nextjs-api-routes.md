# Next.js API Routes Skill

## Purpose
This skill helps create Next.js API routes following best practices.

## Usage
When asked to create API endpoints in Next.js, use this skill to:
- Create API routes in the app/api directory
- Implement proper request/response handling
- Follow REST conventions
- Include error handling and validation
- Use appropriate HTTP methods

## Guidelines
1. Place API routes in app/api/[route]/route.ts (Next.js 13+ App Router)
2. Export GET, POST, PUT, DELETE handlers as needed
3. Use zod for request validation when appropriate
4. Implement proper error responses with correct status codes
5. Follow RESTful API design principles
6. Include rate limiting considerations where appropriate
7. Secure endpoints with authentication when needed