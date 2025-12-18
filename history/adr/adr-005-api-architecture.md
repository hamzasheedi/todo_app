# ADR-005: API Architecture

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-19
- **Feature:** 003-multi-user-todo
- **Context:** Need to design an API architecture that provides consistent, secure, and efficient communication between frontend and backend while enforcing user isolation and proper error handling.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

- Architecture Style: Stateless REST under /api/
- HTTP Status Codes: Consistent usage (200, 201, 400, 401, 403, 404)
- Error Format: Standardized JSON format with message and error code fields
- Sorting Implementation: Backend sorting with query parameters for efficiency
- User Isolation: Validate user_id in URL matches JWT subject for all endpoints
- Response Format: Success/error wrapper with consistent structure

## Consequences

### Positive

- Standard, predictable API behavior that's well-understood
- Consistent error handling across all endpoints
- Efficient server-side sorting reduces frontend processing
- Defense-in-depth security with dual validation
- Clear separation of success/error responses
- Good performance with backend-optimized queries

### Negative

- REST may be less efficient for complex nested queries compared to GraphQL
- Server-side sorting may not be as flexible as client-side for advanced UI interactions
- More complex validation logic required on backend
- Potential over-fetching compared to more granular API approaches

## Alternatives Considered

Alternative A: GraphQL API with Apollo
- Why rejected: More complex for this use case, unnecessary overhead for simple todo operations

Alternative B: RPC-style API
- Why rejected: Less standard and predictable, harder to document and consume

Alternative C: WebSocket-based real-time API
- Why rejected: More complex than needed for this application, over-engineering for basic todo functionality

## References

- Feature Spec: @specs/003-multi-user-todo/spec.md
- Implementation Plan: @specs/003-multi-user-todo/plan.md
- Related ADRs: ADR-002 (Backend Technology Stack), ADR-003 (Authentication Strategy)
- Evaluator Evidence: @specs/003-multi-user-todo/research.md