# ADR-004: Database Architecture

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-19
- **Feature:** 003-multi-user-todo
- **Context:** Need to select a database solution that provides scalability, security, type safety, and proper user isolation for the multi-user todo application.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

- Database Provider: Neon Serverless PostgreSQL
- ORM: SQLModel
- Data Modeling: UUID primary keys, foreign key relationships for user ownership
- Indexing Strategy: Index on user_id for efficient user-based queries, created_date, updated_date, status
- User Isolation: All queries must filter by authenticated user's ID
- Migration Strategy: SQLModel-based migration system

## Consequences

### Positive

- Serverless PostgreSQL provides automatic scaling and cost efficiency
- SQLModel provides excellent type safety and integration with FastAPI
- Proper foreign key constraints ensure data integrity
- Efficient indexing for common query patterns
- Built-in user isolation at database level
- ACID compliance for data consistency

### Negative

- Dependency on Neon's serverless platform
- Potential cold start latency for serverless database
- Learning curve for SQLModel if team is more familiar with other ORMs
- Vendor lock-in to PostgreSQL-specific features

## Alternatives Considered

Alternative A: Raw SQL with psycopg2
- Why rejected: Less type safety, more manual work, no built-in validation

Alternative B: MongoDB with PyMongo
- Why rejected: Less suitable for relational data model with user ownership, no built-in foreign key constraints

Alternative C: SQLite with SQLAlchemy Core
- Why rejected: Less scalable for multi-user application, no serverless option

## References

- Feature Spec: @specs/003-multi-user-todo/spec.md
- Implementation Plan: @specs/003-multi-user-todo/plan.md
- Related ADRs: ADR-002 (Backend Technology Stack)
- Evaluator Evidence: @specs/003-multi-user-todo/research.md