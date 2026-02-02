---
name: api_designer
description: Design and implement RESTful APIs for the Phase II Todo Full-Stack Web Application using FastAPI, SQLModel, and proper authentication patterns.
---

# API Designer Skill

## Purpose

This skill should be used when designing and implementing RESTful APIs for the Phase II Todo Full-Stack Web Application. The skill focuses on creating secure, efficient, and well-documented APIs using FastAPI, SQLModel, and Better Auth integration with consistent error handling and user isolation.

## When to Use This Skill

Use this skill when:
- Designing new API endpoints for the todo application
- Implementing authentication-protected routes with Better Auth integration
- Creating database schemas and API models with SQLModel
- Designing consistent error handling and response formats
- Implementing backend sorting and filtering capabilities
- Ensuring user isolation and proper validation

## How to Use This Skill

### API Endpoint Design Process
1. Define endpoint paths following REST conventions under /api/
2. Implement proper HTTP status codes (200, 201, 400, 401, 403, 404)
3. Create request/response Pydantic models using SQLModel integration
4. Implement authentication validation using dependency injection
5. Add proper user isolation validation (JWT subject vs URL parameter)

### Database Schema Design
1. Create SQLModel models with proper relationships and constraints
2. Define UUID primary keys and foreign key relationships for user ownership
3. Implement proper indexing strategies for efficient queries
4. Add created_date, updated_date, and status fields as needed
5. Create migration scripts for schema changes

### Authentication Integration
1. Implement Better Auth dependencies for route protection
2. Validate user_id in URL matches JWT subject for all user-specific endpoints
3. Handle token refresh and validation automatically
4. Implement proper session management with stateless authentication
5. Create custom exceptions for authentication failures

## Available Resources

### API Templates
- Use templates in `/backend/api/templates/` for creating new endpoints
- Follow established patterns for consistency
- Include proper Pydantic models for request/response validation

### Database Models
- Use models in `/backend/models/` for creating new SQLModel schemas
- Follow established patterns for user ownership and relationships
- Include proper validation and constraints

### Authentication Patterns
- Reference `/backend/auth/templates/` for authentication integration
- Follow established patterns for dependency injection
- Ensure proper validation strategies

### Documentation Templates
- Use `/docs/api_templates/` for API documentation
- Follow OpenAPI/Swagger conventions
- Include proper error response examples

## Output Standards

When designing API implementations:
1. Ensure all endpoints follow REST conventions and are properly secured
2. Include proper error handling with consistent response formats
3. Implement user isolation with dual validation (JWT + URL parameter)
4. Use SQLModel for database operations with proper relationships
5. Document all endpoints with proper request/response examples