# ADR-002: Backend Technology Stack

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-19
- **Feature:** 003-multi-user-todo
- **Context:** Need to select a backend technology stack that provides type safety, security, performance, and easy integration with the chosen frontend and database technologies.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

- Framework: FastAPI
- ORM: SQLModel
- API Architecture: Stateless REST under /api/
- Authentication: JWT verification middleware
- Error Handling: Standardized JSON format with user-friendly messages
- Validation: Pydantic schemas for request/response

## Consequences

### Positive

- Excellent type safety with Python type hints
- Automatic API documentation generation (Swagger/OpenAPI)
- Fast performance comparable to Node.js frameworks
- Strong integration between FastAPI and SQLModel
- Built-in validation and serialization with Pydantic
- Excellent developer experience with automatic error documentation

### Negative

- Python ecosystem may be less familiar to some developers
- Potential performance limitations for extremely high-load scenarios
- Less mature ecosystem compared to Node.js/Express
- Potential complexity in deployment compared to Node.js

## Alternatives Considered

Alternative Stack A: Node.js + Express + Sequelize + JWT
- Why rejected: Less type safety, more manual validation work, less automatic documentation

Alternative Stack B: Node.js + NestJS + TypeORM + Passport
- Why rejected: More complex setup, heavier framework overhead

Alternative Stack C: Go + Gin + GORM + JWT
- Why rejected: Would require different language expertise, less ORM integration

## References

- Feature Spec: @specs/003-multi-user-todo/spec.md
- Implementation Plan: @specs/003-multi-user-todo/plan.md
- Related ADRs: ADR-001 (Frontend Technology Stack)
- Evaluator Evidence: @specs/003-multi-user-todo/research.md