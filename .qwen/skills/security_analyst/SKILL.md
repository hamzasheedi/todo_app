---
name: security_analyst
description: Analyze and implement security measures for the Phase II Todo Full-Stack Web Application including authentication validation, user isolation, input sanitization, and vulnerability assessment.
---

# Security Analyst Skill

## Purpose

This skill should be used when analyzing and implementing security measures for the Phase II Todo Full-Stack Web Application. The skill focuses on identifying vulnerabilities, implementing secure coding practices, and ensuring proper authentication and authorization mechanisms.

## When to Use This Skill

Use this skill when:
- Implementing authentication and authorization controls
- Conducting security reviews of API endpoints
- Designing user isolation mechanisms
- Implementing input validation and sanitization
- Performing vulnerability assessments
- Securing database connections and queries
- Implementing secure session management

## How to Use This Skill

### Security Assessment Process
1. Analyze authentication flow for potential vulnerabilities
2. Review user isolation mechanisms for completeness
3. Examine API endpoints for proper authorization
4. Check for proper input validation and sanitization
5. Verify database query security and prevention of injection attacks
6. Assess session management and token security

### Security Implementation
1. Implement proper JWT validation with Better Auth integration
2. Design dual validation for user identity (JWT subject vs URL parameter)
3. Apply input sanitization using Pydantic validation
4. Implement proper error handling without information disclosure
5. Design secure database connection patterns
6. Create security monitoring and logging mechanisms

### Vulnerability Prevention
1. Prevent SQL injection through parameterized queries and ORM usage
2. Implement CSRF protection for web forms
3. Apply proper CORS policies for API security
4. Design rate limiting for API endpoints
5. Implement secure password hashing and storage
6. Create secure backup and recovery procedures

## Available Resources

### Security Checklists
- Use `/assets/checklists/security_checklist.md` for comprehensive security reviews
- Follow OWASP Top 10 guidelines for vulnerability prevention
- Apply authentication security best practices

### Security Templates
- Use `/templates/security_controls/` for implementing security measures
- Follow established patterns for validation and sanitization
- Include proper logging and monitoring templates

### Vulnerability Testing
- Reference `/tests/security/` for security testing procedures
- Implement automated security scanning
- Conduct penetration testing scenarios

### Compliance Guidelines
- Follow `/guidelines/compliance.md` for regulatory requirements
- Apply privacy protection measures
- Ensure data protection standards compliance

## Output Standards

When performing security analysis:
1. Ensure all authentication mechanisms follow defense-in-depth principles
2. Implement proper user isolation with dual validation
3. Apply input validation and sanitization consistently
4. Create secure error handling without sensitive information disclosure
5. Document security controls and verification procedures
6. Maintain audit trails for security-relevant events