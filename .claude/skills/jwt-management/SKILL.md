---
name: jwt-management
description: Implement comprehensive JWT token lifecycle management with security best practices, refresh strategies, and token rotation
---

# JWT Management Skill

## Purpose

This skill should be used when implementing comprehensive JWT token lifecycle management with security best practices, refresh strategies, and token rotation for the Phase II Todo Full-Stack Web Application. The skill focuses on creating secure, reliable, and efficient JWT token systems.

## When to Use This Skill

Use this skill when:
- Implementing JWT token generation and validation
- Creating token refresh and rotation mechanisms
- Setting up secure token storage and transmission
- Implementing token blacklisting and revocation
- Adding token expiration and renewal strategies
- Ensuring JWT security best practices

## How to Use This Skill

### JWT Token Generation
1. Implement secure JWT token generation with strong algorithms (RS256/ES256)
2. Include proper claims (sub, exp, iat, iss, etc.)
3. Add custom claims for application-specific data
4. Implement proper token signing with secure keys
5. Include token versioning for future compatibility
6. Add proper token size optimization
7. Ensure compliance with JWT standards

### Token Refresh and Rotation
1. Implement refresh token functionality with sliding expiration
2. Create token rotation with refresh token invalidation
3. Add refresh token storage with proper security
4. Implement automatic refresh 5 minutes before expiration
5. Add refresh token validation and security checks
6. Include proper error handling for refresh failures
7. Implement secure refresh token rotation

### Token Security
1. Implement secure token storage (HTTP-only cookies vs secure localStorage)
2. Add CSRF protection for JWT tokens
3. Implement token replay attack prevention
4. Add token binding and validation
5. Include proper token transmission over HTTPS
6. Implement token blacklisting for logout
7. Add security headers for token protection

### Frontend Token Management
1. Implement secure token storage in frontend
2. Add automatic token refresh mechanisms
3. Create token state management with React Context
4. Implement proper token attachment to API requests
5. Add token validation and error handling
6. Include proper cleanup on logout
7. Implement token monitoring and alerts

### Backend Token Validation
1. Create JWT verification middleware
2. Implement proper token validation and parsing
3. Add token expiration checking
4. Include user identity validation
5. Implement token blacklisting verification
6. Add proper error handling for invalid tokens
7. Include comprehensive logging and monitoring

### Token Lifecycle Management
1. Implement proper token creation and issuance
2. Add token refresh and renewal processes
3. Create token revocation and invalidation
4. Implement token cleanup and garbage collection
5. Add token audit and monitoring
6. Include proper error recovery procedures
7. Ensure token consistency across services

## Available Resources

### JWT Utilities
- Use `/backend/auth/utils.py` for token utilities
- Follow established patterns for consistency
- Include proper security and validation
- Implement comprehensive token management

### Authentication Configuration
- Reference `/backend/auth/config.py` for JWT configuration
- Follow established patterns for consistency
- Include proper security parameters
- Implement proper validation and error checking

### Frontend Token Management
- Use `/frontend/lib/api-client.ts` for token management
- Reference `/frontend/components/AuthWrapper.tsx` for state management
- Follow established patterns for consistency
- Include proper error handling and validation

### Security Utilities
- Reference `/backend/utils/security.py` for security functions
- Follow established patterns for consistency
- Include proper validation and sanitization
- Implement comprehensive security measures

## Output Standards

When implementing JWT management:
1. Ensure secure token generation with strong algorithms
2. Include comprehensive refresh and rotation mechanisms
3. Implement proper security measures and validation
4. Use consistent patterns across all token operations
5. Document all JWT processes with proper examples
6. Implement proper monitoring and logging
7. Optimize for security and performance
8. Follow JWT security best practices and standards
9. Test all token scenarios thoroughly including edge cases
10. Maintain comprehensive security and compliance standards