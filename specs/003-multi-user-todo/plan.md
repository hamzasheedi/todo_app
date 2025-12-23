# Implementation Plan: Phase II – Multi-User Full-Stack Todo Web Application

**Feature**: 003-multi-user-todo
**Created**: 2025-12-19
**Status**: Draft
**Plan Version**: 1.0

## Technical Context

**Frontend Stack**: Next.js 16+ with App Router, TypeScript, Tailwind CSS
**Backend Stack**: FastAPI, SQLModel ORM
**Database**: Neon Serverless PostgreSQL
**Authentication**: Better Auth with JWT tokens
**API Architecture**: Stateless REST under /api/
**Spec Compliance**: @specs/003-multi-user-todo/spec.md

## Constitution Check

This implementation plan complies with the project constitution by:
- Following the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code
- Ensuring all code is generated via Claude Code (no manual coding)
- Implementing strict user isolation with user_id validation against JWT subject
- Using environment variables for all secrets (no hardcoded values)
- Maintaining clear separation between frontend, backend, and database layers
- Enforcing JWT authentication on all API endpoints
- Using consistent HTTP status codes (200, 201, 400, 401, 403, 404)

## Gates

- [x] Spec completeness: All functional requirements defined (FR-001 to FR-018)
- [x] Constitutional compliance: All constraints from constitution are satisfied
- [x] Architecture feasibility: Technology stack aligns with constitutional requirements
- [x] Security validation: User isolation and authentication requirements are clear

## Phase 0: Research & Requirements Resolution

### Research Tasks

1. **Authentication Implementation Research**
   - Decision: Use Better Auth with JWT middleware for FastAPI
   - Rationale: Aligns with specification requirement and constitutional constraints
   - Alternatives: Custom JWT implementation vs Better Auth (Better Auth chosen for security and maintenance)

2. **Database Schema Design Research**
   - Decision: Use SQLModel with Neon PostgreSQL for user and task models
   - Rationale: Matches architectural constraints and provides proper ORM capabilities
   - Alternatives: Raw SQL vs ORM vs other ORMs (SQLModel chosen for type safety)

3. **Frontend State Management Research**
   - Decision: Use Next.js App Router with server components for data fetching, client components for interactivity
   - Rationale: Leverages Next.js capabilities while maintaining security
   - Alternatives: Client-side state vs server-side rendering (server-side chosen for security)

4. **API Error Handling Research**
   - Decision: Standardized error response format with user-friendly messages
   - Rationale: Matches requirement FR-017 for user-friendly error messages
   - Alternatives: Technical codes vs user messages (user messages chosen per spec)

## Phase 1: Design & Contracts

### Data Model Design

Based on the specification entities, the following data models will be implemented:

**User Model**:
- `id`: UUID (primary key, immutable)
- `email`: String (unique, required)
- `created_date`: DateTime (auto-generated, immutable)
- `updated_date`: DateTime (auto-updated)

**Task Model**:
- `id`: UUID (primary key, immutable)
- `user_id`: UUID (foreign key to User, immutable)
- `title`: String (1-200 characters, required)
- `description`: String (0-1000 characters, optional)
- `status`: Enum ("incomplete", "complete", default: "incomplete")
- `created_date`: DateTime (auto-generated, immutable)
- `updated_date`: DateTime (auto-updated)

### API Contract Design

Based on the specification, the following API endpoints will be implemented:

**Authentication Endpoints** (handled by Better Auth):
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- `POST /api/auth/signout` - User logout

**Task Management Endpoints**:
- `GET /api/{user_id}/tasks` - Get user's tasks with sorting options
- `POST /api/{user_id}/tasks` - Create new task for user
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update specific task
- `DELETE /api/{user_id}/tasks/{id}` - Delete specific task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Mark task as complete/incomplete

### Environment Configuration

**Required Environment Variables**:
- `DATABASE_URL` - Neon PostgreSQL connection string
- `AUTH_SECRET` - Better Auth secret key
- `NEXTAUTH_URL` - Application base URL
- `JWT_SECRET` - JWT signing secret (if needed beyond Better Auth)

## Phase 2: Implementation Phases

### Phase 2A: Foundation Setup
**Dependencies**: None (first phase)

1. Set up Next.js 16+ project with TypeScript and Tailwind CSS
2. Configure project structure with proper src/ organization
3. Set up environment configuration with secrets management
4. Initialize Git repository with proper .gitignore

### Phase 2B: Authentication Foundation
**Dependencies**: Phase 2A

1. Install and configure Better Auth for Next.js
2. Set up JWT verification middleware for FastAPI
3. Implement user registration and login UI components
4. Create authentication state management
5. Test user isolation enforcement

### Phase 2C: Database & Models
**Dependencies**: Phase 2A

1. Set up Neon PostgreSQL database connection
2. Create SQLModel models for User and Task entities
3. Implement database connection pooling and session management
4. Create database migration system
5. Implement user ownership validation at query level

### Phase 2D: Backend API Implementation
**Dependencies**: Phase 2B, Phase 2C

1. Implement FastAPI task endpoints with JWT verification
2. Create user_id validation to ensure proper isolation
3. Implement all required CRUD operations (GET, POST, PUT, DELETE, PATCH)
4. Add sorting functionality for task lists (Newest First, Oldest First, etc.)
5. Implement proper error handling and status codes
6. Add automatic JWT refresh functionality

### Phase 2E: Frontend UI Integration
**Dependencies**: Phase 2B, Phase 2D

1. Create responsive UI components for task management
2. Implement task sorting controls (Newest First, Oldest First, etc.)
3. Create task creation, viewing, updating, and deletion interfaces
4. Implement task completion toggle functionality
5. Add user-friendly error messaging
6. Ensure mobile-first responsive design with WCAG 2.1 AA compliance

### Phase 2F: Integration & Validation
**Dependencies**: All previous phases

1. End-to-end testing of user authentication flow
2. Validation of user isolation (cross-user access prevention)
3. Task functionality testing across all operations
4. Responsive design validation across breakpoints (768px, 1024px)
5. JWT refresh functionality testing
6. Error handling validation

## Component Breakdown

### Frontend Components
- `AuthWrapper` - Authentication state provider
- `TaskList` - Display and sort tasks with filtering options
- `TaskItem` - Individual task display and interaction
- `TaskForm` - Create and update task interface
- `AuthPage` - Login and registration UI
- `Layout` - Responsive layout with mobile-first design
- `ErrorDisplay` - User-friendly error messages with action items

### Backend Modules
- `auth/` - JWT verification middleware and user validation
- `models/` - SQLModel database models
- `schemas/` - Pydantic request/response schemas
- `routes/tasks.py` - Task management API endpoints
- `database/` - Database connection and session management
- `utils/` - Helper functions for validation and error handling

### Database Schema
- `users` table - User account information
- `tasks` table - User-specific tasks with foreign key to users
- Proper indexing for efficient querying and sorting
- Constraints to enforce data integrity

## Dependencies & Sequencing

### Critical Path Dependencies
1. **Database Models** → **Backend API** → **Frontend Integration**
2. **Authentication** → **All API endpoints** (required for security)
3. **API Contract** → **Frontend API calls** (interface definition)

### Parallelizable Components
- Frontend UI components can be developed while API is being implemented
- Database schema and authentication can be developed in parallel
- Testing can begin as soon as API endpoints are available

## Design Decisions Needing Documentation

### 1. JWT Verification Strategy
- **Decision**: Use dependency injection approach in FastAPI with custom dependency
- **Rationale**: Provides consistent validation across all endpoints while maintaining clean code
- **Alternative**: Middleware vs Dependency Injection (dependency chosen for flexibility)

### 2. User ID Validation in API Routes
- **Decision**: Validate both JWT subject and URL user_id parameter to ensure match
- **Rationale**: Provides defense-in-depth security by checking both identity sources
- **Alternative**: JWT-only vs Dual validation (dual chosen for security)

### 3. Frontend State Management
- **Decision**: Server components for data fetching, client components for interactivity
- **Rationale**: Leverages Next.js App Router while maintaining security by keeping sensitive data on server
- **Alternative**: Client-side state vs Server-side rendering (hybrid chosen for security/performance)

### 4. Error Response Format
- **Decision**: Standardized JSON format with message and error code fields
- **Rationale**: Enables consistent error handling in frontend while providing user-friendly messages
- **Alternative**: Raw error vs Structured response (structured chosen for UX)

### 5. Task Sorting Implementation
- **Decision**: Backend sorting with query parameters for efficiency
- **Rationale**: Reduces frontend processing and ensures consistent sorting across sessions
- **Alternative**: Client-side vs Server-side sorting (server-side chosen for performance)

## Testing & Validation Strategy

### API Validation
- Authentication required validation (401 responses for unauthenticated requests)
- User isolation validation (403 responses for cross-user access attempts)
- JWT token validation (proper token format and expiration handling)
- Input validation (proper error responses for invalid data)

### Frontend Behavior Validation
- Responsive design validation across breakpoints (768px, 1024px)
- User-friendly error message display
- Task sorting functionality validation
- JWT automatic refresh validation
- WCAG 2.1 AA compliance validation

### Error Case Handling
- Database connection failures
- JWT token expiration and refresh
- Network request failures
- Invalid user input validation
- Concurrent access scenarios

### Acceptance Criteria Validation
- User Story 1: Authentication and basic task management
- User Story 2: Secure data isolation
- User Story 3: Persistent task management
- User Story 4: Task sorting and organization
- All functional requirements (FR-001 to FR-018)

## Planning Constraints

- All implementation must follow the Agentic Dev Stack workflow (no manual coding)
- Each task must reference specific requirements from the specification
- All secrets must be managed through environment variables
- Frontend and backend must maintain clear separation
- User isolation must be enforced at every layer (database, API, UI)
- All code must be traceable back to specification requirements

## Success Criteria Validation

The implementation will be considered successful when:
- [ ] Users can sign up and log in (SC-001: 95% success rate)
- [ ] Users can create, view, update, delete, and complete tasks (SC-002: 98% success rate)
- [ ] Each user can access only their own tasks (SC-003: 100% data isolation)
- [ ] Tasks persist across sessions (SC-004: 99% reliability over 30 days)
- [ ] Unauthorized access attempts are blocked (SC-005: 100% blocking)
- [ ] Application works across browsers and screen sizes (SC-006: 95% compatibility)
- [ ] Users complete tasks on first attempt (SC-007: 90% success rate)
- [ ] API endpoints respond with appropriate status codes (SC-008: 99% accuracy)