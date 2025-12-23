---
name: validation-specialist
description: Implement comprehensive multi-layer validation and data integrity checks with security and performance optimization
---

# Validation Specialist Skill

## Purpose

This skill should be used when implementing comprehensive multi-layer validation and data integrity checks with security and performance optimization for the Phase II Todo Full-Stack Web Application. The skill focuses on creating robust, secure, and efficient validation systems across all application layers.

## When to Use This Skill

Use this skill when:
- Implementing input validation and sanitization
- Creating data integrity and business rule validation
- Adding security validation and sanitization
- Implementing performance-optimized validation
- Creating multi-layer validation strategies
- Ensuring data consistency and quality

## How to Use This Skill

### Input Validation Strategy
1. Implement whitelist validation approach for all inputs
2. Create comprehensive validation schemas for all data
3. Add proper type checking and conversion
4. Implement proper sanitization for all inputs
5. Include business rule validation
6. Add cross-field validation requirements
7. Implement validation error messaging

### Frontend Validation
1. Implement client-side validation for user experience
2. Add real-time form validation and feedback
3. Create proper error display and user guidance
4. Implement proper input masking and formatting
5. Add validation before API submission
6. Include accessibility for validation messages
7. Implement proper state management for validation

### Backend Validation
1. Create comprehensive server-side validation
2. Implement proper request/response validation
3. Add database constraint validation
4. Include business logic validation
5. Implement proper error response formatting
6. Add comprehensive logging and monitoring
7. Include security validation and sanitization

### Database Validation
1. Implement proper database constraints
2. Add foreign key and referential integrity
3. Create proper data type validation
4. Include check constraints for business rules
5. Add unique constraints where appropriate
6. Implement proper indexing for validation
7. Include audit trails for validation

### Security Validation
1. Implement SQL injection prevention
2. Add XSS protection with proper output encoding
3. Include CSRF protection validation
4. Add rate limiting and abuse prevention
5. Implement proper authentication validation
6. Add authorization and permission checks
7. Include file upload validation and security

### Performance Optimization
1. Implement efficient validation algorithms
2. Add caching for expensive validation operations
3. Create batch validation for multiple inputs
4. Optimize validation for large datasets
5. Implement lazy validation where appropriate
6. Add validation performance monitoring
7. Include validation result caching

## Available Resources

### Pydantic Schemas
- Use `/backend/schemas/` for Pydantic validation schemas
- Follow established patterns for consistency
- Include proper validation constraints
- Implement comprehensive validation rules

### Validation Utilities
- Reference `/backend/utils/validation.py` for validation utilities
- Follow established patterns for consistency
- Include proper error handling and feedback
- Implement comprehensive validation rules

### Frontend Validation
- Use `/frontend/components/TaskForm.tsx` for form validation
- Follow established patterns for consistency
- Include proper TypeScript interfaces
- Implement proper user feedback and error handling

### Security Utilities
- Reference `/backend/utils/sanitization.py` for input sanitization
- Follow established patterns for consistency
- Include proper security validation
- Implement comprehensive security measures

## Output Standards

When implementing validation systems:
1. Ensure comprehensive validation across all application layers
2. Include proper security validation and sanitization
3. Implement efficient validation algorithms and performance
4. Use consistent patterns across all validation implementations
5. Document all validation rules with proper examples
6. Implement proper error handling and user feedback
7. Optimize for security and performance
8. Follow validation best practices and security standards
9. Test all validation scenarios thoroughly including edge cases
10. Maintain comprehensive validation documentation and monitoring