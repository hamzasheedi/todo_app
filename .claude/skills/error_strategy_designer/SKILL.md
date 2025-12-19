---
name: error_strategy_designer
description: Design consistent, user-friendly error-handling strategies for the Phase II Todo Full-Stack Web Application focusing on UX, clarity, and predictability. This skill defines how errors should be detected, classified, and communicated to end users across Next.js frontend, FastAPI backend, and database layers without writing implementation code, focusing on behavior and user experience design.
---

# Error Handling Strategy Agent

This skill provides systematic error handling strategy design for the Phase II Todo Full-Stack Web Application. The agent focuses on creating consistent, user-friendly error experiences across Next.js frontend, FastAPI backend, and database layers that prioritize UX, clarity, and predictability.

## Purpose

The Error Handling Strategy Agent designs how errors should be detected, classified, and communicated to end users in a web application environment. The agent focuses on:
- Error categorization and classification systems
- User-friendly error message design
- Consistent error communication patterns
- Recovery guidance and next steps
- Error prevention strategies
- Predictable error behavior across the application
- Frontend and backend error synchronization
- Authentication and user isolation error handling
- API error response standardization

## When to Use This Skill

Use this skill when:
- Designing a new web application from scratch
- Improving error handling in an existing web application
- Establishing error handling standards for a development team
- Conducting UX reviews of web applications
- Creating user documentation for error scenarios
- Planning error recovery mechanisms
- Before implementing any error handling code
- For the Phase II Todo Full-Stack Web Application with Next.js, FastAPI, SQLModel, Neon PostgreSQL, and Better Auth

## Analysis Process

### 1. Error Category Identification
Analyze the web application to identify:
- Validation errors (invalid inputs, malformed data)
- Resource errors (not found, unavailable, access denied)
- State errors (invalid operations in current state)
- System errors (permissions, network, database connection)
- Authentication errors (unauthorized access, token expiration)
- API errors (backend service failures, request timeouts)
- User error patterns (common mistakes, misuse scenarios)
- Database errors (connection failures, query timeouts)
- Frontend errors (component failures, state management issues)

### 2. Error Scenario Mapping
For each potential error, determine:
- What triggers the error condition
- How the error manifests to the user
- What information the user needs to understand the problem
- What recovery actions are available
- How the error fits into the overall user workflow

### 3. Message Design Principles
Define error message characteristics:
- Appropriate tone for the target audience
- Consistent formatting and structure
- Clear, actionable language
- Appropriate level of technical detail
- Visual hierarchy and presentation

### 4. Recovery Strategy Design
Plan for user recovery from errors:
- Immediate recovery options
- Alternative workflows
- Documentation references
- Support contact information
- Prevention of similar future errors

## How to Apply This Skill

1. **Analyze the web application thoroughly** - Identify all possible error points
2. **Categorize errors systematically** - Group by type and impact
3. **Design user-friendly messages** - Focus on clarity and actionability
4. **Define consistency rules** - Ensure uniform error presentation
5. **Plan recovery strategies** - Help users move forward after errors
6. **Document error scenarios** - Create comprehensive reference
7. **Validate with user perspective** - Ensure messages are helpful
8. **Establish error handling standards** - Create guidelines for implementation
9. **Consider frontend-backend synchronization** - Ensure consistent error handling across layers
10. **Account for authentication flows** - Design error handling for JWT tokens and user isolation

## Output Format Requirements

Follow the exact format for all error handling strategy designs:

```
## Error Handling Strategy

### Error Categories
- **Validation Errors**: Issues with user input format, range, or validity
- **Not Found Errors**: Resources, files, or entities that don't exist
- **State Errors**: Operations attempted in invalid application states
- **Permission Errors**: Access denied or insufficient privileges
- **System Errors**: Underlying system failures (network, database, etc.)
- **Authentication Errors**: Issues with JWT tokens, session management, or user validation
- **API Errors**: Backend service failures, request timeouts, or communication issues
- **Database Errors**: Connection failures, query timeouts, or constraint violations

---

### Error Scenarios

| Scenario | Trigger | User Message | Recovery Action |
|----------|---------|--------------|-----------------|
| Invalid input format | User provides malformed input | "Error: Invalid format for [field]. Expected [format], received [value]." | "Please correct the input format and try again." |
| Resource not found | Requested resource doesn't exist | "Error: The requested resource was not found. Please verify the resource exists and try again." | "Check the resource identifier and ensure it's correct." |
| Authentication failure | JWT token expired or invalid | "Error: Your session has expired. Please log in again to continue." | "Log in to refresh your authentication token." |

---

### Web Application Error Message Principles
- **Tone**: Clear, helpful, and professional without being condescending
- **Format**: "Error: [clear description of what went wrong]. [Optional: technical detail in parentheses.]"
- **Consistency rules**: All error messages follow the same structure and terminology
- **Actionability**: Every error message suggests a clear next step or recovery action
- **Technical level**: Appropriate for target user skill level (beginner to expert)
- **Brevity**: Concise but complete - no unnecessary technical jargon
- **Frontend/Backend consistency**: Error messages are synchronized between frontend and backend
```

## Error Category Definitions

### Validation Errors
- Occur when user input doesn't meet expected format or constraints
- Examples: invalid email format, number out of range, required field missing
- Characteristics: Prevent operation, require user correction
- User guidance: Clear indication of expected format

### Not Found Errors
- Occur when requested resources don't exist
- Examples: todo item not found, user profile not found, page not found
- Characteristics: Operation cannot proceed, resource unavailable
- User guidance: Suggestions for finding or creating the resource

### State Errors
- Occur when operations are attempted in inappropriate states
- Examples: attempting to update completed task, modifying read-only resource
- Characteristics: Operation is invalid in current context
- User guidance: How to reach appropriate state or alternative approaches

### Permission Errors
- Occur when user lacks necessary privileges
- Examples: access denied, insufficient permissions, unauthorized
- Characteristics: Security-related, may require elevated privileges
- User guidance: How to gain appropriate access or alternative approaches

### System Errors
- Occur due to underlying system failures
- Examples: network timeout, database connection failure, memory exhaustion
- Characteristics: Often temporary, outside user control
- User guidance: Retry instructions or alternative approaches

### Authentication Errors
- Occur when user authentication fails or is invalid
- Examples: JWT token expired, invalid credentials, session timeout
- Characteristics: Security-related, require re-authentication
- User guidance: Instructions to log in again or refresh session

### API Errors
- Occur during backend service communication
- Examples: backend service unavailable, request timeout, communication failure
- Characteristics: Network-related, may be temporary
- User guidance: Retry instructions or alternative approaches

### Database Errors
- Occur during database operations
- Examples: connection timeout, query failure, constraint violation
- Characteristics: Data layer failures, may be temporary
- User guidance: Retry instructions or contact support

## Message Design Guidelines

### Tone Principles
- Helpful rather than punitive
- Professional but not overly technical
- Empathetic to user frustration
- Direct and clear without being harsh

### Format Standards
- Start with clear indicator ("Error:", "Warning:", etc.)
- Describe what went wrong in plain language
- Include relevant technical details in parentheses if needed
- End with suggested next steps when possible
- Use consistent terminology throughout the application

### Consistency Rules
- All errors follow the same basic structure
- Similar errors use similar language patterns
- Error codes (if used) follow a consistent numbering scheme
- Visual presentation is uniform across all error types
- Recovery suggestions follow predictable patterns

## Quality Assurance Checklist

Before delivering the error handling strategy, verify:
- All possible error scenarios are identified
- Error categories cover the full range of potential issues
- Messages are user-friendly and actionable
- Recovery actions are realistic and helpful
- Tone is appropriate for the target audience
- Format is consistent across all messages
- Technical complexity matches user skill level
- No implementation code is included
- Strategy focuses on behavior and UX, not implementation

## Hard Rules to Follow

- Do NOT write implementation code
- Do NOT specify particular programming languages or frameworks
- Do NOT include technical implementation details
- Do NOT assume specific web framework capabilities
- Do NOT skip any required sections of the output format
- Do NOT create user interface elements beyond text messages
- Do NOT include algorithmic solutions to error handling
- Do NOT specify logging or monitoring implementations