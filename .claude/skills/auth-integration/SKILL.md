---
name: auth-integration
description: Implement Better Auth integration with JWT token management, automatic refresh, secure session handling, and comprehensive security measures
---

# Authentication Integration Skill

## Purpose

This skill should be used when implementing Better Auth integration with JWT token management, automatic refresh, secure session handling, and comprehensive security measures for the Phase II Todo Full-Stack Web Application. The skill focuses on creating secure, reliable, and user-friendly authentication systems.

## When to Use This Skill

Use this skill when:
- Setting up Better Auth integration with Next.js
- Implementing JWT token lifecycle management
- Creating secure session handling mechanisms
- Implementing token refresh and rotation strategies
- Adding authentication middleware and validation
- Ensuring secure token storage and transmission

## How to Use This Skill

### JWT Token Management
1. Implement secure JWT token generation with strong algorithms
2. Create token refresh mechanisms with sliding expiration
3. Implement token rotation for enhanced security
4. Handle token expiration and renewal automatically
5. Add proper token validation and verification
6. Implement secure token storage and retrieval

### Session Management
1. Create secure session state management
2. Implement proper session invalidation on logout
3. Handle concurrent session management
4. Implement session timeout and cleanup
5. Add session monitoring and security checks
6. Ensure stateless authentication design

### Security Implementation
1. Implement token storage security (HTTP-only cookies vs localStorage)
2. Add CSRF protection for authentication endpoints
3. Implement rate limiting for authentication attempts
4. Add brute force protection mechanisms
5. Implement secure token transmission over HTTPS
6. Add token blacklisting for compromised tokens

### Frontend Integration
1. Integrate with Next.js App Router authentication patterns
2. Implement proper token attachment to API requests
3. Handle authentication state across application components
4. Implement proper error handling for authentication failures
5. Add loading states and user feedback during authentication
6. Ensure consistent authentication experience across the app

### Backend Validation
1. Implement JWT verification middleware
2. Validate user_id in URL matches JWT subject
3. Add proper authentication dependency injection
4. Implement comprehensive error handling
5. Add logging and monitoring for authentication events
6. Ensure consistent validation across all protected endpoints

## Available Resources

### Authentication Templates
- Use templates in `/backend/auth/templates/` for JWT middleware
- Follow established patterns for consistency
- Include proper validation and error handling
- Implement secure token handling procedures

### Frontend Integration
- Reference `/frontend/lib/api-client.ts` for token management
- Use `/frontend/components/AuthWrapper.tsx` for state management
- Follow established patterns for consistency
- Include proper error handling and user feedback

### Security Utilities
- Use `/backend/utils/security.py` for security utilities
- Implement proper validation and sanitization
- Follow security best practices and guidelines
- Include proper logging and monitoring

### Configuration
- Reference `.env.example` for secure environment configuration
- Use `/backend/auth/config.py` for authentication settings
- Follow established patterns for consistency
- Include proper validation and error checking

## Output Standards

When implementing authentication systems:
1. Ensure all tokens are generated with strong cryptographic algorithms
2. Implement automatic token refresh 5 minutes before expiration
3. Include proper validation and error handling across all layers
4. Use secure token storage and transmission methods
5. Document all authentication flows with proper examples
6. Implement comprehensive security measures and monitoring
7. Optimize for performance while maintaining security
8. Follow security best practices and prevent common vulnerabilities
9. Test authentication flows thoroughly including edge cases
10. Implement proper session management and cleanup procedures