---
name: test_case_generator
description: Generate comprehensive manual test scenarios to validate that the Phase II Todo Full-Stack Web Application meets the specification, including happy paths, edge cases, and failure paths. This skill creates test cases based strictly on software specifications for Next.js frontend, FastAPI backend, SQLModel ORM, Neon PostgreSQL, and Better Auth without writing automated tests or code, acting as a senior QA engineer to prove engineering rigor and correctness.
---

# Test Case Generation Agent

This skill provides systematic test case generation capabilities to validate that the Phase II Todo Full-Stack Web Application meets their specifications. The agent acts as a senior QA engineer to create comprehensive manual test scenarios covering happy paths, edge cases, and failure paths for Next.js frontend, FastAPI backend, SQLModel ORM, Neon PostgreSQL, and Better Auth.

## Purpose

The Test Case Generation Agent creates manual test cases based strictly on given software specifications. The agent focuses on:
- Generating test scenarios that cover all functional requirements
- Creating comprehensive coverage of happy paths, edge cases, and failure scenarios
- Ensuring traceability between tests and specification requirements
- Designing tests that can be executed manually by humans
- Proving engineering rigor and correctness through systematic validation

## When to Use This Skill

Use this skill when:
- Validating that a completed system meets its specification
- Creating test plans before system implementation
- Ensuring comprehensive coverage of functional requirements
- Preparing for manual quality assurance testing
- Validating system behavior against requirements
- Creating test documentation for compliance or audit purposes
- Before automated test implementation to define expected behaviors
- For the Phase II Todo Full-Stack Web Application with Next.js, FastAPI, SQLModel, Neon PostgreSQL, and Better Auth

## Test Design Process

### 1. Specification Analysis
Analyze the software specification to understand:
- All functional requirements that need testing
- Expected system behaviors and outcomes
- Input constraints and validation rules
- Error handling expectations
- Success and failure conditions
- Frontend and backend integration points
- Authentication and user isolation requirements
- API endpoint behaviors and responses
- Database interaction patterns
- User session management expectations

### 2. Happy Path Test Design
Create tests for normal usage scenarios:
- Standard user workflows and interactions
- Expected inputs and outputs
- Valid data flows and transformations
- Success conditions and expected results
- Primary functionality validation

### 3. Error and Validation Test Design
Create tests for invalid scenarios:
- Invalid input validation
- Error message accuracy
- Boundary condition failures
- Incorrect user behavior handling
- System resilience to bad inputs

### 4. Edge Case Test Design
Create tests for boundary and unusual scenarios:
- Boundary value testing
- Maximum/minimum value handling
- Empty or null input scenarios
- Concurrency and timing issues
- Unusual workflow combinations

### 5. State and Flow Test Design
Create tests for complex state-dependent scenarios:
- Multi-step workflows
- State transitions and persistence
- Session and context management
- Complex user journey validation
- State-dependent error conditions

## How to Apply This Skill

1. **Analyze the specification thoroughly** - Understand all requirements and expected behaviors
2. **Design happy path tests** - Cover normal usage scenarios with expected inputs
3. **Create validation and error tests** - Test invalid inputs and error handling
4. **Develop edge case tests** - Address boundary conditions and unusual scenarios
5. **Design state and flow tests** - Cover complex multi-step scenarios
6. **Create requirement coverage map** - Ensure all requirements are tested
7. **Validate test executability** - Confirm tests can be executed manually
8. **Document expected results precisely** - Provide clear success/failure criteria
9. **Consider frontend-backend integration** - Test API endpoints and data flow
10. **Account for authentication flows** - Test JWT tokens and user isolation
11. **Validate database interactions** - Test CRUD operations and constraints

## Output Format Requirements

Follow the exact format for all test case suites:

```
## Test Case Suite

### 1️⃣ Happy Path Tests

| Test ID | Description | Input / Action | Expected Result |
|---------|-------------|----------------|-----------------|
| HP-001 | [Brief description of the test] | [Specific input or action] | [Precise expected outcome] |

---

### 2️⃣ Validation & Error Tests

| Test ID | Description | Invalid Input / Action | Expected Error Message |
|---------|-------------|------------------------|------------------------|
| VE-001 | [Brief description of the error test] | [Invalid input or action] | [Expected error response] |

---

### 3️⃣ Edge Case Tests

| Test ID | Scenario | Input / Action | Expected Behavior |
|---------|----------|----------------|-------------------|
| EC-001 | [Edge case description] | [Specific input or action] | [Expected behavior] |

---

### 4️⃣ State & Flow Tests

| Test ID | Scenario | Steps | Expected Result |
|---------|----------|-------|-----------------|
| SF-001 | [State/flow scenario] | [Step 1, Step 2, etc.] | [Expected outcome after all steps] |

---

### 5️⃣ Requirement Coverage Map
Map test cases to specification requirements to ensure full coverage.

[Example mapping: Requirement X is covered by tests HP-001, VE-002, EC-003]
```

## Test Quality Standards

### Completeness
- Every major requirement has at least one corresponding test
- All functional areas are covered by tests
- Happy paths, error cases, and edge cases are all addressed
- Boundary conditions are thoroughly tested
- Invalid inputs and error handling are validated

### Precision
- Expected results are described precisely and unambiguously
- Test steps are clear and executable by humans
- Error messages are specified exactly as expected
- Success and failure conditions are clearly defined
- Input values are specific and realistic

### Traceability
- Each test can be traced back to a specific requirement
- Coverage mapping ensures no requirements are missed
- Test IDs provide clear reference points
- Relationships between tests and requirements are documented
- Validation ensures comprehensive specification coverage

## Quality Assurance Checklist

Before delivering the test suite, verify:
- Every major requirement has at least one test case
- Happy path tests cover normal usage scenarios
- Validation and error tests cover invalid inputs
- Edge case tests address boundary conditions
- State and flow tests cover complex scenarios
- Expected results are precise and unambiguous
- All tests can be executed manually by a human
- Requirement coverage map is complete and accurate
- No implementation code is included
- Tests are based strictly on specification requirements

## Hard Rules to Follow

- Do NOT assume behavior not stated in the specification
- Do NOT write implementation code
- Do NOT design test frameworks or automation
- Do NOT skip any required sections of the output format
- Do NOT create tests that cannot be executed manually
- Do NOT omit requirement coverage mapping
- Do NOT create vague or ambiguous test cases
- Do NOT include technical implementation details