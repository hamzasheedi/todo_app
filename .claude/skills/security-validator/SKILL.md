---
name: security-validator
description: Validate and enforce comprehensive security measures including user isolation, authentication enforcement, input validation, and cross-user access prevention
---

# Security Validator Skill

## Purpose

This skill should be used when validating and enforcing comprehensive security measures including user isolation, authentication enforcement, input validation, and cross-user access prevention for the Phase II Todo Full-Stack Web Application. The skill focuses on creating secure, resilient, and protected applications following security best practices.

## When to Use This Skill

Use this skill when:
- Implementing security validation and enforcement mechanisms
- Ensuring user isolation and data protection
- Adding input validation and sanitization
- Implementing authentication and authorization
- Conducting security audits and vulnerability assessments
- Preventing common security vulnerabilities

## How to Use This Skill

### Authentication Validation
1. Implement comprehensive JWT token validation
2. Validate user_id in URL matches JWT subject
3. Add proper authentication dependency injection
4. Implement multi-factor authentication where appropriate
5. Add session management and invalidation
6. Include proper error handling for authentication failures
7. Implement secure token storage and transmission

### User Isolation
1. Ensure all database queries filter by authenticated user ID
2. Implement proper validation of user ownership
3. Add cross-user access prevention at all layers
4. Create proper authentication dependency injection
5. Include comprehensive validation and error handling
6. Ensure data security and privacy compliance
7. Test user isolation thoroughly

### Input Validation and Sanitization
1. Implement whitelist validation approach
2. Add comprehensive input sanitization
3. Prevent SQL injection with parameterized queries
4. Add XSS protection with proper output encoding
5. Implement CSRF protection with tokens
6. Add rate limiting and abuse prevention
7. Include file upload validation and security

### Security Testing
1. Conduct penetration testing and vulnerability assessments
2. Perform security code reviews
3. Test authentication and authorization mechanisms
4. Validate user isolation and data protection
5. Test input validation and sanitization
6. Assess security configuration and settings
7. Document security findings and remediation

### Security Monitoring
1. Implement comprehensive security logging
2. Add intrusion detection and monitoring
3. Monitor authentication and authorization events
4. Track security-relevant activities
5. Implement security alerting and notifications
6. Create security dashboards and reports
7. Establish incident response procedures

## Available Resources

### Security Utilities
- Use `/backend/utils/security.py` for security utilities
- Implement proper validation and sanitization
- Follow security best practices and guidelines
- Include proper logging and monitoring

### Validation Utilities
- Reference `/backend/utils/validation.py` for validation utilities
- Follow established patterns for consistency
- Include proper error handling and feedback
- Implement comprehensive validation rules

### Security Middleware
- Use `/backend/middleware/security.py` for security middleware
- Implement proper validation and error handling
- Follow established patterns for consistency
- Include comprehensive security checks

### Security Guidelines
- Reference `/assets/security_checklist.md` for security validation
- Follow established patterns for consistency
- Include proper validation and testing
- Implement comprehensive security measures

## Output Standards

When implementing security measures:
1. Ensure all validation follows whitelist approach and security best practices
2. Include comprehensive authentication and authorization validation
3. Implement proper input sanitization and output encoding
4. Use secure coding practices and prevent common vulnerabilities
5. Document all security measures with proper examples and testing
6. Implement comprehensive security logging and monitoring
7. Optimize for security while maintaining performance
8. Follow security best practices and prevent common vulnerabilities
9. Test all security measures thoroughly including penetration testing
10. Maintain security compliance and privacy regulations