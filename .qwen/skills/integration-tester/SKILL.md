---
name: integration-tester
description: Implement comprehensive integration tests validating complete user flows, cross-layer functionality, and system resilience
---

# Integration Tester Skill

## Purpose

This skill should be used when implementing comprehensive integration tests validating complete user flows, cross-layer functionality, and system resilience for the Phase II Todo Full-Stack Web Application. The skill focuses on creating thorough, reliable, and maintainable integration testing strategies that validate the complete system behavior.

## When to Use This Skill

Use this skill when:
- Creating integration tests for cross-layer functionality
- Validating complete user journey scenarios
- Testing API and database integration
- Implementing end-to-end testing procedures
- Validating authentication and authorization flows
- Testing system resilience and error handling

## How to Use This Skill

### Integration Test Strategy
1. Create comprehensive test scenarios for complete user flows
2. Implement cross-layer integration testing
3. Validate API and database interactions
4. Test authentication and authorization integration
5. Verify user isolation and data security
6. Test error handling across system layers
7. Include performance validation in integration tests

### User Journey Testing
1. Test complete user registration and login flows
2. Validate task creation and management workflows
3. Test authentication and session management
4. Verify data persistence across sessions
5. Test user isolation and cross-user access prevention
6. Validate responsive design across user flows
7. Include accessibility validation in user journeys

### API Integration Testing
1. Test API endpoints with real database connections
2. Validate request/response handling across layers
3. Test authentication token integration
4. Verify error handling and status codes
5. Test API rate limiting and security measures
6. Validate data validation and sanitization
7. Include performance testing for API integrations

### Database Integration Testing
1. Test database operations with real connections
2. Validate foreign key relationships and constraints
3. Test transaction handling and rollbacks
4. Verify data integrity and consistency
5. Test concurrent database access
6. Validate database migration integration
7. Include performance testing for database operations

### Security Integration Testing
1. Test authentication and authorization integration
2. Validate user isolation across all layers
3. Test input validation and sanitization integration
4. Verify secure token handling
5. Test security headers and protections
6. Validate error message security
7. Include penetration testing in integration scenarios

### Performance and Resilience Testing
1. Test system behavior under load conditions
2. Validate error recovery and resilience
3. Test timeout and retry mechanisms
4. Verify graceful degradation capabilities
5. Test resource utilization under load
6. Include failure scenario testing
7. Monitor system performance during integration tests

## Available Resources

### Integration Test Suites
- Use `/tests/integration/` for comprehensive integration tests
- Follow established patterns for consistency
- Include proper test organization and structure
- Implement comprehensive validation procedures

### Backend Integration Tests
- Reference `/backend/test/` for backend integration testing
- Follow established patterns for consistency
- Include proper test data and fixtures
- Implement comprehensive backend validation

### Frontend Integration Tests
- Use `/frontend/test/` for frontend integration testing
- Follow established patterns for consistency
- Include proper component testing
- Implement comprehensive UI validation

### End-to-End Tests
- Reference `/tests/e2e/` for end-to-end test scenarios
- Follow established patterns for consistency
- Include proper user journey validation
- Implement comprehensive flow testing

## Output Standards

When implementing integration testing:
1. Ensure comprehensive validation of cross-layer functionality
2. Include complete user journey validation
3. Implement proper test data management and cleanup
4. Use consistent test organization and naming conventions
5. Document all integration test scenarios with proper examples
6. Implement proper test environment management
7. Optimize for fast and reliable test execution
8. Follow integration testing best practices and methodologies
9. Test all system interactions thoroughly including edge cases
10. Maintain comprehensive test documentation and reporting