# ADR-003: Authentication Strategy

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-19
- **Feature:** 003-multi-user-todo
- **Context:** Need to implement secure user authentication with JWT tokens that enforces user isolation and provides automatic token refresh for a seamless user experience.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

- Authentication Provider: Better Auth
- Token Type: JWT tokens
- Validation Strategy: Dependency injection approach in FastAPI with custom dependency
- User ID Validation: Validate both JWT subject and URL user_id parameter to ensure match
- Token Refresh: Automatic refresh with background renewal 5 minutes before expiration
- Session Management: Stateless authentication (no server-side session storage)

## Consequences

### Positive

- Production-ready authentication with proper security practices
- Built-in support for common authentication flows
- Defense-in-depth security by checking both JWT and URL parameters
- Seamless user experience with automatic token refresh
- Stateless architecture reduces server memory requirements
- Consistent validation across all endpoints

### Negative

- Dependency on third-party authentication provider
- Potential vendor lock-in to Better Auth ecosystem
- Complexity in managing token refresh logic
- Additional network calls for token validation

## Alternatives Considered

Alternative A: Custom JWT implementation with manual middleware
- Why rejected: Higher maintenance and security risks, more prone to implementation errors

Alternative B: Session-based authentication with server-side storage
- Why rejected: Does not align with stateless architecture requirements, more complex scaling

Alternative C: OAuth2 with multiple providers
- Why rejected: More complex than needed for this application, over-engineering for simple email/password auth

## References

- Feature Spec: @specs/003-multi-user-todo/spec.md
- Implementation Plan: @specs/003-multi-user-todo/plan.md
- Related ADRs: ADR-001 (Frontend Technology Stack), ADR-002 (Backend Technology Stack)
- Evaluator Evidence: @specs/003-multi-user-todo/research.md