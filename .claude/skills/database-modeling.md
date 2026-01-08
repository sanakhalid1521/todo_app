# Database Modeling Skill

## Purpose
This skill helps create proper database models using SQLModel for the todo application.

## Usage
When asked to create or modify database models, use this skill to:
- Define models using SQLModel (SQLAlchemy + Pydantic)
- Implement proper relationships between models
- Add appropriate constraints and indexes
- Design for scalability and performance
- Follow existing model patterns

## Guidelines
1. Always inherit from SQLModel for database models
2. Use UUID primary keys with gen_random_uuid() default
3. Implement proper foreign key relationships
4. Add appropriate indexes for query optimization
5. Include created_at and updated_at timestamps with timezone awareness
6. Use proper field constraints (nullable, unique, etc.)
7. Implement proper cascade options for relationships
8. Follow the existing model patterns in the project
9. Ensure proper validation with Pydantic field validators if needed
10. Consider data migration strategies when modifying existing models