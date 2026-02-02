---
name: backend-architect
description: Design and implement FastAPI backend architecture with SQLModel ORM, JWT authentication middleware, and secure API endpoints following RESTful principles
---

# Backend Architect Skill

## Purpose

This skill should be used when designing and implementing FastAPI backend architecture with SQLModel ORM, JWT authentication middleware, and secure API endpoints for the Phase II Todo Full-Stack Web Application. The skill focuses on creating secure, efficient, and well-documented APIs following RESTful principles and modern best practices.

## When to Use This Skill

Use this skill when:
- Designing new API endpoints for the todo application
- Implementing authentication-protected routes with JWT integration
- Creating database schemas and API models with SQLModel
- Designing consistent error handling and response formats
- Implementing backend security measures and validation
- Optimizing database queries and API performance

## How to Use This Skill

### API Endpoint Design Process
1. Define endpoint paths following REST conventions under /api/
2. Implement proper HTTP status codes (200, 201, 400, 401, 403, 404)
3. Create request/response Pydantic models using SQLModel integration
4. Implement authentication validation using dependency injection
5. Add proper user isolation validation (JWT subject vs URL parameter)
6. Include comprehensive input validation and sanitization

### Database Schema Design
1. Create SQLModel models with proper relationships and constraints
2. Define UUID primary keys and foreign key relationships for user ownership
3. Implement proper indexing strategies for efficient queries
4. Add created_date, updated_date, and status fields as needed
5. Create migration scripts for schema changes
6. Implement proper connection pooling and session management

### Security Implementation
1. Implement JWT authentication dependencies for route protection
2. Validate user_id in URL matches JWT subject for all user-specific endpoints
3. Handle token validation and refresh automatically
4. Implement proper session management with stateless authentication
5. Create custom exceptions for authentication failures
6. Add rate limiting and security middleware

### Performance Optimization
1. Optimize database queries with proper indexing
2. Implement caching strategies for frequently accessed data
3. Use async/await patterns for non-blocking operations
4. Implement proper pagination for large datasets
5. Add request/response logging for performance monitoring
6. Implement proper error handling and logging

## Available Resources

### API Templates
- Use templates in `/backend/api/templates/` for creating new endpoints
- Follow established patterns for consistency
- Include proper Pydantic models for request/response validation
- Implement proper error handling and documentation

### Database Models
- Use models in `/backend/models/` for creating new SQLModel schemas
- Follow established patterns for user ownership and relationships
- Include proper validation and constraints
- Implement proper indexing strategies

### Authentication Patterns
- Reference `/backend/auth/templates/` for authentication integration
- Follow established patterns for dependency injection
- Ensure proper validation strategies
- Implement secure token handling

### Middleware and Utilities
- Use `/backend/middleware/` for common functionality
- Implement logging, error handling, and security middleware
- Follow established patterns for consistency
- Include proper documentation and examples

## Output Standards

When designing backend implementations:
1. Ensure all endpoints follow REST conventions and are properly secured
2. Include proper error handling with consistent response formats
3. Implement user isolation with dual validation (JWT + URL parameter)
4. Use SQLModel for database operations with proper relationships
5. Document all endpoints with proper request/response examples
6. Implement proper logging and monitoring
7. Optimize for performance and scalability
8. Follow security best practices and prevent common vulnerabilities