<!--
Sync Impact Report:
- Version change: 1.4.0 → 1.4.1
- Modified principles: XX. Logging & Monitoring
- Added sections: XXVIII. AI Fail-Safe Behavior, XXIX. Feedback Awareness
- Removed sections: None
- Templates requiring updates:
  - .specify/templates/plan-template.md ⚠ pending
  - .specify/templates/spec-template.md ⚠ pending
  - .specify/templates/tasks-template.md ⚠ pending
  - .specify/templates/commands/*.md ⚠ pending
- Follow-up TODOs: None
-->

# Todo App Feature Progression Constitution

## Core Principles

### I. Incremental Development
Each phase builds on the previous, from Basic → Intermediate → Advanced → AI Chatbot features. All development follows a progressive enhancement approach where each level adds capabilities to the foundation without breaking existing functionality.

### II. Spec-Driven Implementation
All code must be generated via Claude Code and Spec-Kit Plus, not handwritten. Every implementation step must map back to an explicit requirement in the specification before any code is written.

### III. Modularity & Maintainability
Features must be self-contained and minimally coupled, maintainable code modules. Code components should be designed with clear separation of concerns and minimal coupling between modules.

### IV. Usability & Clarity
Intuitive CLI or UI, consistent patterns, clear feedback. Task management interactions must be intuitive and clearly documented. User interfaces and CLI commands should follow consistent patterns and provide clear feedback for all operations.

### V. Reliability & State Consistency
Task states must always reflect correct values. Tasks and status updates should always reflect the correct state, even after multiple operations. The system must maintain data integrity and provide consistent behavior across all operations.

### VI. Automation & Intelligence
Advanced phases should incorporate AI-driven automation where appropriate. The system should evolve from simple CLI operations to intelligent, event-driven, distributed platform capabilities with AI chatbot functionality.

### VII. Spec-First Development (Phase II)
No implementation without a written, approved spec. Specs are the single source of truth for all development activities in Phase II and beyond.

### VIII. Agentic Workflow Integrity (Phase II)
Follow the workflow strictly: Write spec → Generate plan → Break into tasks → Implement. No manual coding outside Claude Code execution in Phase II and beyond.

### IX. Security by Default (Phase II & AI Chatbot)
All data access must be authenticated. User isolation is enforced at every layer in the multi-user system. All user requests must be authenticated via Better Auth; sensitive data must never be exposed in responses.

### X. Separation of Concerns (Phase II)
Frontend, backend, database, and auth are clearly separated. Cross-layer behavior is coordinated only through specs in Phase II architecture.

### XI. Production-Realism (Phase II & AI Chatbot)
Decisions must reflect real-world SaaS practices. Avoid shortcuts that would not scale beyond a demo in Phase II implementation. Architecture must allow adding new MCP tools or commands without major refactoring.

### XII. Natural Language Usability (AI Chatbot - Phase III)
Chatbot must interpret and execute user commands accurately and intuitively. The system must respond to all natural language commands with appropriate task operations.

### XIII. Stateless Architecture Compliance (AI Chatbot - Phase III)
Conversation state is persisted to database; server holds no in-memory state. Each request must be independent; server should allow horizontal scaling and restarts without data loss.

### XIV. MCP-Driven Task Management (AI Chatbot - Phase III)
All task operations (add, list, update, complete, delete) must be performed exclusively via MCP tools. Each task operation must invoke the correct MCP tool with proper parameters.

### XV. AI Integration Consistency (AI Chatbot - Phase III)
All AI logic routed through OpenAI Agents SDK via Gemini API (base_url). All AI calls must use configured base_url pointing to Gemini API.

### XVI. Reliability & Error Handling (AI Chatbot - Phase III)
Graceful handling of missing tasks, invalid commands, and database errors. Return clear error messages for missing tasks or invalid operations.

### XVII. Confirmation & Clarity (AI Chatbot - Phase III)
Agent responses must confirm actions in a user-friendly manner. Responses should be concise, human-readable, and context-aware.

### XVIII. Security & Access Control (AI Chatbot - Phase III)
All user requests must be authenticated via Better Auth; sensitive data must never be exposed in responses.

### XIX. Extensibility (AI Chatbot - Phase III)
Architecture must allow adding new MCP tools or commands without major refactoring.

### XX. Logging & Monitoring (AI Chatbot - Phase III)
All tool invocations and errors must be logged for debugging and quality improvement. Track all MCP tool invocations and errors specifically for debugging and quality improvement purposes.

### XXI. Performance (AI Chatbot - Phase III)
API responses should be returned within reasonable latency (<500ms ideally) to ensure smooth user experience.

### XXII. Testing & Validation (AI Chatbot - Phase III)
All tool calls and AI responses must be testable and reproducible for QA purposes.

### XXIII. Data Integrity (AI Chatbot - Phase III)
All database operations must ensure consistency; no partial updates or lost data.

### XXIV. Versioning (AI Chatbot - Phase III)
MCP tools and API endpoints should be versioned to avoid breaking changes.

### XXV. Accessibility (AI Chatbot - Phase III)
Chatbot responses should be readable and understandable to users with varying technical backgrounds.

### XXVI. Rate Limiting & Abuse Prevention (AI Chatbot - Phase III)
Implement safeguards to prevent excessive or malicious requests.

### XXVII. Audit Trail (AI Chatbot - Phase III)
Maintain history of all task modifications with timestamps and user IDs for accountability.

### XXVIII. AI Fail-Safe Behavior (AI Chatbot - Phase III)
Provide clear fallback responses if AI or MCP tool fails to execute a command, so the user always receives guidance. The system must gracefully handle tool failures and communicate appropriate next steps to the user.

### XXIX. Feedback Awareness (AI Chatbot - Phase III)
Log AI misinterpretations or errors to support future improvements in NLP accuracy. The system must capture and store feedback data about AI performance to enable iterative improvements to natural language processing capabilities.

## Feature Completion Standards

### Basic Level Requirements
- Add Task: Create new tasks with title and description
- Delete Task: Remove tasks from the system
- Update Task: Modify task properties and content
- View Task List: Display all tasks with current status
- Mark as Complete: Update task completion status

### Intermediate Level Requirements
- Priorities & Tags/Categories: Organize tasks with priority levels and category tags
- Search & Filter: Find tasks based on content, status, or metadata
- Sort Tasks: Arrange task lists by various criteria (date, priority, etc.)

### Advanced Level Requirements
- Recurring Tasks: Create tasks that repeat on scheduled intervals
- Due Dates & Time Reminders: Schedule tasks with deadlines and notification capabilities

### AI Chatbot Level Requirements (Phase III)
- Natural Language Processing: Interpret user commands in natural language
- MCP Tool Integration: Execute task operations exclusively via MCP tools
- Conversation Persistence: Store and retrieve conversation history
- AI Accuracy: Match intended commands with correct tool invocations
- User Experience: Provide friendly, actionable confirmations for all operations

## Spec-Driven Development Standards

### Agentic Dev Stack Workflow
- Follow Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code
- Maintain all spec files in `/specs_history`
- All code files should reference the Spec ID they implement

### Development Constraints
- No manual coding allowed; all code must be generated via spec-driven AI tools
- Each phase must demonstrate fully functional features before progressing
- Testing and validation required for all implemented features

### Development Constraints (Phase II)
- ❌ No manual edits to source code
- ❌ No undocumented endpoints
- ❌ No hardcoded secrets
- ❌ No shared database sessions between frontend and backend
- ✅ All secrets via environment variables
- ✅ All logic traceable to a spec

### Required Spec Types (Phase II)
- Feature specs → /specs/features/
- API specs → /specs/api/
- Database specs → /specs/database/
- UI specs → /specs/ui/

### Referencing Rules (Phase II)
- Always reference specs using @specs/...
- If behavior is unclear, update the spec before coding
- Specs must be updated when requirements change

## Coding Standards

### Technology Requirements
- Python 3.13+ compliant
- Clean code principles and PEP compliance
- Proper folder structure: `/src`, `/specs_history`, `README.md`, `CLAUDE.md`

### Code Quality
- Follow established Python best practices and PEP standards
- Include comprehensive error handling and validation
- Implement proper input sanitization and security measures

## Architectural Standards (Phase II & AI Chatbot)

### Frontend
- Framework: OpenAI Agents SDK ChatKit, domain allowlist configured for deployment
- Language: TypeScript
- Authentication handled exclusively via Better Auth
- API access only through a centralized API client
- JWT token automatically attached to all backend requests

### Backend
- Framework: FastAPI
- ORM: SQLModel
- API style: RESTful
- MCP server with Official MCP SDK
- Authentication: JWT verification middleware
- No frontend session dependencies
- All routes under /api/

### Database
- Provider: Neon Serverless PostgreSQL
- Schema defined only in /specs/database
- Migrations must reflect spec changes
- User ownership enforced via user_id foreign key

## Authentication & Authorization Rules (Phase II & AI Chatbot)

Authentication is mandatory for all API endpoints. JWT tokens:
- Issued by Better Auth
- Verified by FastAPI using shared secret

Backend must:
- Reject unauthenticated requests (401 Unauthorized)
- Reject cross-user access (403 Forbidden)
- Ensure user_id in URL must match JWT subject
- Never trust client-provided user identity without token verification

## API Behavior Constraints (Phase II & AI Chatbot)

- Stateless backend
- JWT required on every request
- All task queries filtered by authenticated user
- CRUD operations must validate task ownership
- Consistent HTTP status codes:
  - 200 success
  - 201 created
  - 400 validation error
  - 401 unauthenticated
  - 403 unauthorized
  - 404 not found

## Quality Standards (Phase II & AI Chatbot)

- Clear error messages (developer-friendly)
- Predictable API responses
- Idempotent operations where applicable
- Defensive validation at API boundaries
- No duplicated business logic across layers
- Conversations accurately stored and retrievable
- Responses match intended commands with correct tool invocations

## Documentation Standards

### Required Documentation
- README.md: Setup instructions and usage examples
- CLAUDE.md: Instructions for generating and updating code via Claude Code
- Spec files: Clear requirements, acceptance criteria, and implementation plans

### Documentation Quality
- Documentation must be clear, comprehensive, consistent, and up-to-date
- Include examples for all major functionality
- Maintain consistency in terminology and formatting

## Success Criteria

### Phase I: Basic Features
- Fully functional CLI app with all Basic features implemented and validated
- Functional demonstration of Add, Delete, Update, View, and Mark Complete operations

### Phase II: Intermediate Features
- All Intermediate features implemented and functional
- Functional demonstration of Priorities & Tags/Categories, Search & Filter, and Sort Tasks

### Phase III: Advanced Features
- Advanced features implemented, tested, and validated
- Functional demonstration of Recurring Tasks and Due Dates & Time Reminders
- Project exhibits clear evolution from simple in-memory CLI to potential cloud-native AI system

### Phase IV: Multi-User Full-Stack Todo Web Application
- All 5 basic task features work end-to-end
- Multi-user support with strict data isolation
- JWT authentication fully enforced
- Frontend and backend deploy independently
- All behavior is spec-traceable
- No unauthenticated access possible
- Agentic Dev Stack workflow is demonstrable and reviewable

### Phase V: AI Chatbot Integration (Todo AI Chatbot - Phase III)
- Functional Compliance: All task operations work via MCP tools as specified.
- Conversation Persistence: Chat history accurately stored and retrievable.
- AI Accuracy: Responses match intended commands with correct tool invocations.
- User Experience: Friendly, actionable confirmations for all operations.
- Stateless Resilience: Server can restart or scale without losing conversation or task integrity.
- Natural language commands properly handled and executed.
- MCP tools correctly integrated for all task operations.
- AI Fail-Safe Behavior: AI responds gracefully when a task operation fails.
- Monitoring & Logging: All tool calls and errors are logged for debugging and quality improvement.
- Feedback Awareness: Basic feedback data is available to iteratively improve AI accuracy.

## Governance

All development must comply with this constitution. Amendments require explicit documentation, stakeholder approval, and migration plans. The constitution is the single source of truth for project governance.

**Version**: 1.4.1 | **Ratified**: 2025-12-17 | **Last Amended**: 2025-12-24