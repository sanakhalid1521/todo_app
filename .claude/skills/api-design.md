# API Design Skill

## Purpose
This skill helps create well-designed API endpoints following REST principles and the existing architecture.

## Usage
When asked to create or modify API endpoints, use this skill to:
- Follow REST conventions for endpoint design
- Implement proper HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Design consistent request/response structures
- Implement proper error handling and status codes
- Follow the existing API patterns in the project

## Guidelines
1. Use FastAPI for endpoint creation
2. Follow the existing route structure in /backend/api/
3. Use proper Pydantic models for request/response validation
4. Implement appropriate HTTP status codes (200, 201, 400, 401, 404, 500, etc.)
5. Follow REST naming conventions for endpoints
6. Implement proper authentication and authorization checks
7. Include comprehensive error handling
8. Use proper dependency injection with Depends()
9. Follow existing patterns for database session management
10. Ensure consistent response formatting
11. Document endpoints with proper descriptions
12. Implement rate limiting where appropriate