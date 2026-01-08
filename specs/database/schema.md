# Database Schema Specification

## Overview
This document specifies the database schema for the Todo application using SQLModel with Neon Serverless PostgreSQL.

## Database Technology
- Primary: Neon Serverless PostgreSQL
- ORM: SQLModel (SQLAlchemy + Pydantic)
- Connection: AsyncSession for asynchronous operations

## Table Definitions

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Todos Table
```sql
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## SQLModel Models

### User Model
- id: UUID, primary key, auto-generated
- email: String, unique, not nullable
- password: String, not nullable
- name: String, not nullable
- created_at: DateTime, timezone-aware, auto-generated
- updated_at: DateTime, timezone-aware, auto-generated
- todos: Relationship to Todo model (one-to-many)

### Todo Model
- id: UUID, primary key, auto-generated
- title: String, not nullable
- description: Text, nullable
- completed: Boolean, default false
- user_id: UUID, foreign key to User, cascading delete
- created_at: DateTime, timezone-aware, auto-generated
- updated_at: DateTime, timezone-aware, auto-generated
- user: Relationship to User model (many-to-one)

## Indexes
- Index on users.email for fast login
- Index on todos.user_id for efficient user-based queries
- Index on todos.completed for filtering completed tasks

## Constraints
- Foreign key constraint on todos.user_id references users.id
- Unique constraint on users.email
- Cascade delete on user deletion removes associated todos

## Migration Strategy
- Alembic for database migrations
- Automatic schema initialization on startup
- Environment-specific configuration for development/production

## Connection Pooling
- AsyncSession for concurrent connections
- Connection timeout and retry configuration
- Health check endpoints for database connectivity