# Error Handling Patterns and Strategies Reference

## Error Classification System

### 1. Client Errors (4xx equivalent)
- **Validation Errors**: Invalid input format, missing required fields
- **Authentication Errors**: Invalid credentials, expired tokens
- **Authorization Errors**: Insufficient permissions, access denied
- **Resource Errors**: Item not found, already exists

### 2. Server Errors (5xx equivalent)
- **System Errors**: Database connection failures, network timeouts
- **Internal Errors**: Unexpected exceptions, programming errors
- **Resource Errors**: Out of memory, disk space issues
- **Service Errors**: Downstream service failures

### 3. Application Errors
- **Business Logic Errors**: Violation of business rules
- **State Errors**: Invalid operation in current state
- **Constraint Errors**: Database constraints, business rules

## Common Error Handling Patterns

### 1. Fail-Fast Pattern
- Validate inputs early in the process
- Return errors immediately when detected
- Prevent invalid data from propagating

### 2. Graceful Degradation
- Continue operating with reduced functionality
- Provide fallback mechanisms
- Maintain core functionality when possible

### 3. Circuit Breaker Pattern
- Prevent cascading failures
- Temporarily stop requests to failing services
- Gradually resume operations when possible

## Error Message Design Guidelines

### 1. User-Friendly Messages
- Use clear, non-technical language
- Explain what went wrong in user terms
- Provide actionable next steps
- Avoid exposing internal implementation details

### 2. Developer-Friendly Messages
- Include error codes for debugging
- Provide technical details in logs
- Maintain consistency across error types
- Support internationalization when needed

### 3. Message Structure
```
[Error Level]: [Brief Description] - [Detailed Explanation] [Error Code]
```

## CLI-Specific Error Patterns

### 1. Input Validation Errors
- Invalid argument format
- Missing required arguments
- Conflicting arguments
- Out-of-range values

### 2. Resource Access Errors
- File not found
- Permission denied
- Network connectivity issues
- Service unavailable

### 3. State Errors
- Invalid operation in current context
- Operation not allowed in current state
- Prerequisites not met
- Session expired

## Recovery Strategy Patterns

### 1. Automatic Recovery
- Retry failed operations with exponential backoff
- Use fallback values or services
- Implement circuit breakers

### 2. Manual Recovery
- Provide clear recovery instructions
- Suggest alternative approaches
- Offer remediation tools or commands

### 3. Prevention Strategies
- Input validation and sanitization
- Pre-flight checks
- Health monitoring and alerts

## Error Logging and Monitoring

### 1. Log Structure
- Error code and type
- Timestamp and context
- User and session information
- Stack trace (for developers)

### 2. Monitoring Metrics
- Error rate by type
- Recovery success rate
- Mean time to recovery
- User impact metrics

## Common Error Scenarios and Solutions

### 1. Network-Related Errors
- **Scenario**: Remote service unavailable
- **Solution**: Retry with backoff, use cache, provide offline mode

### 2. Authentication Errors
- **Scenario**: Token expired or invalid
- **Solution**: Prompt for re-authentication, auto-refresh if possible

### 3. Resource Limit Errors
- **Scenario**: Rate limit exceeded, quota reached
- **Solution**: Inform user, suggest retry time, offer upgrade path

### 4. Data Validation Errors
- **Scenario**: Invalid input format
- **Solution**: Show specific field and expected format