---
name: error-handling-specialist
description: Implement comprehensive error handling with user-friendly messages, proper status codes, graceful failure management, and error monitoring
---

# Error Handling Specialist Skill

## Purpose

This skill should be used when implementing comprehensive error handling with user-friendly messages, proper status codes, graceful failure management, and error monitoring for the Phase II Todo Full-Stack Web Application. The skill focuses on creating robust, user-friendly, and maintainable error handling systems.

## When to Use This Skill

Use this skill when:
- Implementing error handling across frontend and backend
- Creating user-friendly error messages and displays
- Designing error recovery and fallback mechanisms
- Setting up error monitoring and logging systems
- Handling API failures and network errors
- Implementing graceful degradation strategies

## How to Use This Skill

### Frontend Error Handling
1. Implement React error boundaries at component level
2. Create user-friendly error display components
3. Add proper loading and error states for async operations
4. Implement graceful error recovery mechanisms
5. Include clear user guidance for error recovery
6. Add retry mechanisms for transient failures
7. Implement proper error logging and reporting

### Backend Error Handling
1. Create comprehensive exception handling middleware
2. Implement proper HTTP status code responses
3. Add detailed error logging with context
4. Create standardized error response formats
5. Implement proper validation error handling
6. Add authentication and authorization error handling
7. Include security-aware error responses

### Error Response Formats
1. Implement consistent error response structure
2. Include proper error codes and messages
3. Add detailed error context for debugging
4. Implement user-friendly messages for end users
5. Include technical details for developers
6. Add proper error correlation IDs
7. Ensure security by not exposing sensitive information

### Monitoring and Logging
1. Implement structured logging with proper context
2. Add error correlation across request chains
3. Create error dashboards and alerting systems
4. Implement error rate monitoring and alerting
5. Add error trending and pattern analysis
6. Create error reporting for user feedback
7. Include performance impact tracking

### User Experience Considerations
1. Provide clear, actionable error messages
2. Include recovery suggestions and next steps
3. Implement graceful degradation for non-critical errors
4. Add visual indicators for error states
5. Include proper accessibility for error messages
6. Implement consistent error styling and UX
7. Add error prevention through validation

### Error Recovery Strategies
1. Implement automatic retry mechanisms for transient errors
2. Add circuit breaker patterns for external services
3. Create fallback mechanisms for service degradation
4. Implement graceful degradation of features
5. Add user notification for error resolution
6. Include error state persistence and recovery
7. Create error handling documentation for users

## Available Resources

### Error Display Components
- Use `/frontend/components/ErrorDisplay.tsx` for error components
- Follow established patterns for consistency
- Include proper TypeScript interfaces for props
- Implement proper accessibility attributes

### Backend Error Utilities
- Reference `/backend/utils/error_handlers.py` for backend error handling
- Follow established patterns for consistency
- Include proper logging and context
- Implement standardized response formats

### API Client Error Handling
- Use `/frontend/lib/api-client.ts` for API error handling
- Follow established patterns for consistency
- Include proper retry logic and fallbacks
- Implement proper error correlation and logging

### Error Middleware
- Reference `/backend/middleware/error_handler.py` for global error handling
- Follow established patterns for consistency
- Include proper logging and monitoring
- Implement comprehensive error handling

## Output Standards

When implementing error handling:
1. Ensure consistent error response formats across all layers
2. Include comprehensive error logging and monitoring
3. Implement user-friendly error messages with clear guidance
4. Use proper HTTP status codes and error responses
5. Document all error handling patterns with proper examples
6. Implement proper error correlation and tracing
7. Optimize for user experience and recovery
8. Follow error handling best practices and security standards
9. Test all error scenarios thoroughly including edge cases
10. Maintain comprehensive error documentation and monitoring