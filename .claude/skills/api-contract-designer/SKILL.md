---
name: api-contract-designer
description: Design and implement RESTful API contracts with proper endpoints, validation, error handling, authentication enforcement, and comprehensive documentation
---

# API Contract Designer Skill

## Purpose

This skill should be used when designing and implementing RESTful API contracts with proper endpoints, validation, error handling, authentication enforcement, and comprehensive documentation for the Phase II Todo Full-Stack Web Application. The skill focuses on creating well-documented, consistent, and maintainable APIs following industry best practices.

## When to Use This Skill

Use this skill when:
- Designing new API endpoints following REST conventions
- Creating comprehensive request/response validation
- Implementing consistent error handling and response formats
- Adding authentication and authorization to endpoints
- Generating API documentation and specifications
- Ensuring API consistency and maintainability

## How to Use This Skill

### API Design Process
1. Define endpoint paths following REST conventions under /api/
2. Implement proper HTTP status codes (200, 201, 400, 401, 403, 404)
3. Create request/response Pydantic models with comprehensive validation
4. Implement authentication validation using dependency injection
5. Add proper user isolation validation (JWT subject vs URL parameter)
6. Include comprehensive input validation and sanitization
7. Follow HATEOAS principles where appropriate

### Request/Response Validation
1. Create comprehensive Pydantic schemas for all request/response objects
2. Implement proper validation constraints and error messages
3. Add custom validators for complex business logic
4. Include proper type hints and documentation
5. Validate all input parameters and query strings
6. Implement proper serialization and deserialization
7. Add proper error response formats

### Error Handling
1. Implement consistent error response format across all endpoints
2. Include proper error codes, messages, and details
3. Add proper logging for error tracking and monitoring
4. Implement graceful error recovery where possible
5. Include user-friendly error messages
6. Add proper debugging information for development
7. Ensure security by not exposing sensitive information

### Documentation
1. Generate automatic OpenAPI documentation
2. Include comprehensive endpoint descriptions
3. Add proper request/response examples
4. Document authentication requirements
5. Include error response examples
6. Add proper API versioning information
7. Maintain up-to-date documentation

## Available Resources

### API Templates
- Use templates in `/backend/api/templates/` for creating new endpoints
- Follow established patterns for consistency
- Include proper Pydantic models for request/response validation
- Implement proper error handling and documentation

### Schema Definitions
- Use schemas in `/backend/schemas/` for request/response models
- Follow established patterns for consistency
- Include proper validation and constraints
- Implement proper documentation and examples

### Documentation Templates
- Use `/docs/api_templates/` for API documentation
- Follow OpenAPI/Swagger conventions
- Include proper error response examples
- Maintain comprehensive endpoint documentation

### Response Utilities
- Reference `/backend/utils/responses.py` for standardized responses
- Use established patterns for consistency
- Include proper formatting and validation
- Follow best practices for API responses

## Output Standards

When designing API contracts:
1. Ensure all endpoints follow REST conventions and are properly documented
2. Include comprehensive request/response validation with proper error handling
3. Implement user isolation with dual validation (JWT + URL parameter)
4. Use consistent error response formats across all endpoints
5. Document all endpoints with proper request/response examples
6. Implement proper authentication and authorization
7. Optimize for performance and scalability
8. Follow security best practices and prevent common vulnerabilities
9. Maintain comprehensive API documentation
10. Test API contracts thoroughly including error scenarios