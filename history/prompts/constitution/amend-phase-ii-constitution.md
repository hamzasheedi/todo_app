---
id: constitution-amend-phase-ii-20251218-001
stage: constitution
title: "amend-phase-ii-constitution"
date: 2025-12-18
author: Claude
feature:
status: completed
---

# Constitution Amendment: Phase II Multi-User Full-Stack Todo Web Application

## Summary

This PHR documents the amendment to the Todo App Feature Progression Constitution to include Phase II requirements for a Multi-User Full-Stack Todo Web Application using Next.js, FastAPI, SQLModel, Neon PostgreSQL, and Better Auth.

## Amendment Details

The constitution was updated to include:
- New core principles for Phase II (Spec-First Development, Agentic Workflow Integrity, Security by Default, Separation of Concerns, Production-Realism)
- Architectural standards for frontend (Next.js), backend (FastAPI), and database (Neon PostgreSQL)
- Authentication & Authorization rules with JWT enforcement
- API behavior constraints with consistent HTTP status codes
- Quality standards for Phase II
- Success criteria for Phase II Multi-User Full-Stack Todo Web Application

## Changes Made

- Version incremented from 1.2.0 to 1.3.0
- Added 5 new core principles for Phase II
- Added architectural standards sections
- Added authentication and authorization rules
- Added API behavior constraints
- Added quality standards for Phase II
- Added Phase IV success criteria for Multi-User Full-Stack Todo Web Application
- Updated sync impact report in the constitution file

## Validation

The updated constitution has been validated to ensure:
- No duplicate sections exist
- Proper structure and formatting maintained
- All Phase II requirements properly integrated
- Version and date information updated correctly

## Original Prompt

Amendment in constitutionProject Phase II: Multi-User Full-Stack Todo Web Application (Next.js + FastAPI + SQLModel + Neon PostgreSQL + Better Auth) This project evolves an existing Phase I console-based todo application into a secure, production-grade, multi-user web application using spec-driven, agentic development. Core Principles Spec-First Development No implementation without a written, approved spec Specs are the single source of truth Agentic Workflow Integrity Follow the workflow strictly: Write spec → Generate plan → Break into tasks → Implement No manual coding outside Claude Code execution Security by Default All data access must be authenticated User isolation is enforced at every layer Separation of Concerns Frontend, backend, database, and auth are clearly separated Cross-layer behavior is coordinated only through specs Production-Realism Decisions must reflect real-world SaaS practices Avoid shortcuts that would not scale beyond a demo Architectural Standards Frontend Framework: Next.js 16+ (App Router) Language: TypeScript Styling: Tailwind CSS Authentication handled exclusively via Better Auth API access only through a centralized API client JWT token automatically attached to all backend requests Backend Framework: FastAPI ORM: SQLModel API style: RESTful Authentication: JWT verification middleware No frontend session dependencies All routes under /api/ Database Provider: Neon Serverless PostgreSQL Schema defined only in /specs/database Migrations must reflect spec changes User ownership enforced via user_id foreign key Authentication & Authorization Rules Authentication is mandatory for all API endpoints JWT tokens: Issued by Better Auth Verified by FastAPI using shared secret Backend must: Reject unauthenticated requests (401 Unauthorized) Reject cross-user access (403 Forbidden) user_id in URL must match JWT subject Never trust client-provided user identity without token verification Spec-Driven Standards Required Spec Types Feature specs → /specs/features/ API specs → /specs/api/ Database specs → /specs/database/ UI specs → /specs/ui/ Referencing Rules Always reference specs using @specs/... If behavior is unclear, update the spec before coding Specs must be updated when requirements change Development Constraints ❌ No manual edits to source code ❌ No undocumented endpoints ❌ No hardcoded secrets ❌ No shared database sessions between frontend and backend ✅ All secrets via environment variables ✅ All logic traceable to a spec API Behavior Constraints Stateless backend JWT required on every request All task queries filtered by authenticated user CRUD operations must validate task ownership Consistent HTTP status codes: 200 success 201 created 400 validation error 401 unauthenticated 403 unauthorized 404 not found Quality Standards Clear error messages (developer-friendly) Predictable API responses Idempotent operations where applicable Defensive validation at API boundaries No duplicated business logic across layers Success Criteria The Phase II project is considered successful when: ✅ All 5 basic task features work end-to-end ✅ Multi-user support with strict data isolation ✅ JWT authentication fully enforced ✅ Frontend and backend deploy independently ✅ All behavior is spec-traceable ✅ No unauthenticated access possible ✅ Agentic Dev Stack workflow is demonstrable and reviewable Evaluation Focus prioritize: Spec clarity and completeness Correct use of Spec-Kit Plus conventions Proper Claude Code delegation Security correctness Architectural discipline Real-world feasibility

## Response Summary

The constitution was successfully updated with all Phase II requirements, including new principles, architectural standards, authentication rules, and success criteria. The version was updated to 1.3.0, and all duplicate sections were resolved.