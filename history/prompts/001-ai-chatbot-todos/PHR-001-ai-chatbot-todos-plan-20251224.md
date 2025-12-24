---
id: PHR-001-ai-chatbot-todos-plan-20251224
title: AI Chatbot Plan Complete
stage: plan
date: 2025-12-24
surface: todo_app
model: Claude Sonnet 4.5
feature: 001-ai-chatbot-todos
branch: 001-ai-chatbot-todos
user: Hamza
command: /sp.plan
labels: [ai-chatbot, plan, mcp, gemini, chatkit]
links:
  spec: specs/001-ai-chatbot-todos/spec.md
  ticket:
  adr:
  pr:
files:
  - specs/001-ai-chatbot-todos/plan.md
  - specs/001-ai-chatbot-todos/research.md
  - specs/001-ai-chatbot-todos/data-model.md
  - specs/001-ai-chatbot-todos/quickstart.md
  - specs/001-ai-chatbot-todos/contracts/chat-api.yaml
  - specs/001-ai-chatbot-todos/contracts/task-api.yaml
tests:
  - plan-validation: PASSED
  - constitution-check: PASSED
  - spec-compliance: PASSED
---

## Prompt

Todo AI Chatbot (Phase III)
Analyze the approved Feature Specification: Todo AI Chatbot – Phase III (Basic Level Functionality) and produce a clear, execution-ready plan covering the following:
1. High-Level Architecture Plan
Describe the end-to-end flow between ChatKit UI, FastAPI backend, OpenAI Agents SDK (via Gemini  api and base_url), MCP Server, and Neon PostgreSQL.
Clarify stateless request handling and where state is persisted.
Identify agent boundaries vs MCP tool responsibilities.


2. Implementation Phases
Organize work into sequential phases aligned with Agentic Dev Stack:
Phase A: Agent & MCP tool specification alignment
Phase B: Backend chat endpoint + persistence flow
Phase C: MCP tool wiring for task operations
Phase D: Frontend ChatKit integration
Phase E: Error handling, confirmations, and logging

3. Task Breakdown (No Code)
Break each phase into concrete, reviewable tasks suitable for Claude Code execution.
Ensure all Functional Requirements (FR-001 to FR-013) are traceable to tasks.
Highlight dependencies between tasks.


4. Key Design Decisions to Document
List important decisions with options and tradeoffs, such as:
Conversation pagination strategy
Error handling patterns in stateless agents
Tool invocation ordering (e.g., list → delete)
Conversation context window management

5. Testing & Validation Strategy
Map Acceptance Scenarios and Success Criteria (SC-001 to SC-008) to validation checks.
Define how MCP tool calls, responses, and failures will be verified.
Include restart and statelessness validation.


6. Constraints & Guardrails
No manual coding (Claude Code only)
All AI calls routed through Gemini via configured base_url
MCP tools are the only mechanism for task mutations
Backend must remain stateless at all times

Output Requirements
Structured plan in Markdown
Clear headings and bullet points
No implementation code
Ready to be passed directly into /sp.tasks


Goal: Produce a plan that is simple, auditable, and optimized for todo project, ensuring fast execution without architectural ambiguity.

## Response snapshot

# Implementation Plan: Todo AI Chatbot – Phase III (Basic Level Functionality)

**Branch**: `001-ai-chatbot-todos` | **Date**: 2025-12-24 | **Spec**: @specs/001-ai-chatbot-todos/spec.md
**Input**: Feature specification from `/specs/001-ai-chatbot-todos/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of an AI-powered chatbot interface for managing todos using natural language. The system will integrate OpenAI Agents SDK via Gemini API with MCP server architecture to expose task operations as tools. The backend will remain stateless with all conversation and task state persisted in Neon PostgreSQL. The frontend will use ChatKit UI for natural language interaction with the AI agent.

## Technical Context

**Language/Version**: Python 3.13+, TypeScript for frontend
**Primary Dependencies**: FastAPI, SQLModel, OpenAI Agents SDK (via Gemini API), MCP Server, Neon PostgreSQL, Better Auth, ChatKit UI
**Storage**: Neon Serverless PostgreSQL database with SQLModel ORM
**Testing**: pytest for backend testing, integration tests for MCP tool validation
**Target Platform**: Web application with frontend/backend separation
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <500ms response time for AI interactions, horizontal scaling capability
**Constraints**: Stateless backend (all state in DB), MCP tools only for task mutations, Gemini API routing for all AI calls
**Scale/Scope**: Multi-user support with isolated data, conversation persistence across sessions

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Spec-Driven Implementation (II)**: All code must be generated via Claude Code and Spec-Kit Plus - PASSED (following Agentic Dev Stack workflow)
2. **Agentic Workflow Integrity (VIII)**: Follow workflow strictly: Write spec → Generate plan → Break into tasks → Implement - PASSED (following process)
3. **Security by Default (IX)**: All data access must be authenticated with user isolation - PASSED (Better Auth integration planned)
4. **Stateless Architecture Compliance (XIII)**: Conversation state persisted to database; server holds no in-memory state - PASSED (design requirement)
5. **MCP-Driven Task Management (XIV)**: All task operations must be performed exclusively via MCP tools - PASSED (core requirement)
6. **AI Integration Consistency (XV)**: All AI logic routed through OpenAI Agents SDK via Gemini API - PASSED (design requirement)
7. **Logging & Monitoring (XX)**: All tool invocations and errors must be logged - PASSED (planned requirement)
8. **AI Fail-Safe Behavior (XXVIII)**: Provide clear fallback responses if AI or MCP tool fails - PASSED (design requirement)
9. **Feedback Awareness (XXIX)**: Log AI misinterpretations for future improvements - PASSED (planned requirement)

**Post-Design Constitution Check**: All gates remain PASSED after Phase 1 design completion.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task.py
│   │   ├── conversation.py
│   │   └── message.py
│   ├── services/
│   │   ├── task_service.py
│   │   ├── conversation_service.py
│   │   └── mcp_server.py
│   ├── api/
│   │   ├── chat_endpoints.py
│   │   └── task_endpoints.py
│   └── core/
│       ├── auth.py
│       └── config.py
└── tests/

frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface/
│   │   │   └── ChatKitWrapper.tsx
│   │   └── TaskManagement/
│   │       └── TaskDisplay.tsx
│   ├── pages/
│   │   └── ChatPage.tsx
│   ├── services/
│   │   └── api-client.ts
│   └── context/
│       └── auth-context.ts
└── tests/

specs/
└── 001-ai-chatbot-todos/
    ├── plan.md
    ├── research.md
    ├── data-model.md
    ├── quickstart.md
    ├── contracts/
    └── tasks.md
```

**Structure Decision**: Web application structure selected with clear separation between frontend (React/TypeScript with ChatKit) and backend (FastAPI with SQLModel). Backend handles MCP server for task operations and AI integration via Gemini API. Frontend provides ChatKit UI for natural language interaction.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

## 1. High-Level Architecture Plan

### End-to-End Flow
1. **Frontend (ChatKit UI)**: User interacts via natural language in the ChatKit interface
2. **Backend (FastAPI)**: Receives user messages, maintains authentication, routes to AI agent
3. **AI Agent (OpenAI SDK via Gemini)**: Processes natural language, determines appropriate MCP tool calls
4. **MCP Server**: Executes task operations (add, list, update, complete, delete) via registered tools
5. **Neon PostgreSQL**: Persists tasks, conversations, and messages for state recovery

### State Management
- **Stateless Backend**: FastAPI server maintains no in-memory state
- **Persistent State**: All conversation history and task data stored in Neon PostgreSQL
- **Session Recovery**: Server restarts do not affect user data or conversation context

### Agent Boundaries vs MCP Responsibilities
- **Agent Responsibilities**: Natural language processing, intent recognition, response generation
- **MCP Tool Responsibilities**: Direct task operations (CRUD), data validation, persistence

## 2. Implementation Phases

### Phase A: Agent & MCP Tool Specification Alignment
- Define MCP tool specifications for all task operations
- Align tool parameters with functional requirements
- Set up Gemini API configuration for AI agent

### Phase B: Backend Chat Endpoint + Persistence Flow
- Implement conversation and message models
- Create chat API endpoints with authentication
- Set up database persistence for conversations

### Phase C: MCP Tool Wiring for Task Operations
- Implement MCP server with task operation tools
- Connect tools to database operations
- Add logging and error handling for tool invocations

### Phase D: Frontend ChatKit Integration
- Integrate ChatKit UI with backend API
- Implement authentication flow
- Add user experience enhancements

### Phase E: Error Handling, Confirmations, and Logging
- Implement comprehensive error handling
- Add user confirmations and friendly responses
- Set up logging and monitoring

## 3. Task Breakdown (No Code)

### Phase A: Agent & MCP Tool Specification Alignment
- A1: Define MCP tool specifications for task creation (FR-001)
- A2: Define MCP tool specifications for task listing (FR-002)
- A3: Define MCP tool specifications for task updates (FR-003)
- A4: Define MCP tool specifications for task completion (FR-004)
- A5: Define MCP tool specifications for task deletion (FR-005)
- A6: Configure Gemini API base_url for AI agent (FR-011)
- A7: Validate tool specifications against functional requirements

### Phase B: Backend Chat Endpoint + Persistence Flow
- B1: Create Conversation and Message SQLModel entities (FR-006, FR-007)
- B2: Implement conversation persistence API endpoints
- B3: Create chat endpoint with authentication (FR-014)
- B4: Implement conversation history retrieval
- B5: Set up database migrations for new entities
- B6: Test conversation persistence across server restarts (FR-008)

### Phase C: MCP Tool Wiring for Task Operations
- C1: Implement MCP server infrastructure
- C2: Create add_task MCP tool (FR-001, FR-012)
- C3: Create list_tasks MCP tool (FR-002, FR-012)
- C4: Create update_task MCP tool (FR-003, FR-012)
- C5: Create complete_task MCP tool (FR-004, FR-012)
- C6: Create delete_task MCP tool (FR-005, FR-012)
- C7: Integrate MCP tools with database operations
- C8: Add logging for all MCP tool invocations (FR-010)

### Phase D: Frontend ChatKit Integration
- D1: Set up ChatKit UI component with authentication
- D2: Connect ChatKit to backend chat endpoints
- D3: Implement user authentication flow (FR-014)
- D4: Add loading states and user feedback
- D5: Test natural language command interpretation
- D6: Implement pagination for large task lists (FR-017)

### Phase E: Error Handling, Confirmations, and Logging
- E1: Implement AI fail-safe responses (XXVIII)
- E2: Add friendly confirmation messages for all operations (FR-009)
- E3: Implement error handling for AI service downtime (FR-016)
- E4: Add input validation and character limits (FR-018)
- E5: Set up comprehensive logging for debugging
- E6: Test server restart resilience (FR-008)
- E7: Validate all functional requirements compliance

## 4. Key Design Decisions to Document

### Conversation Pagination Strategy
- **Decision**: Display up to 50 tasks at once with pagination controls
- **Rationale**: Balances user experience with performance
- **Tradeoffs**: More complex UI vs. performance with large datasets

### Error Handling Patterns in Stateless Agents
- **Decision**: All errors handled gracefully with clear user feedback
- **Rationale**: Maintains user confidence when AI or tools fail
- **Tradeoffs**: Additional complexity vs. better user experience

### Tool Invocation Ordering (e.g., list → delete)
- **Decision**: Sequential tool invocation with proper state management
- **Rationale**: Ensures data consistency and proper operation flow
- **Tradeoffs**: Slight latency vs. data integrity

### Conversation Context Window Management
- **Decision**: Store conversation history in database, retrieve as needed
- **Rationale**: Maintains context across sessions while keeping server stateless
- **Tradeoffs**: Database queries vs. memory efficiency

## 5. Testing & Validation Strategy

### Functional Requirement Mapping
- **FR-001 to FR-005**: Validate through MCP tool execution tests
- **FR-006 to FR-008**: Test conversation persistence and server restart resilience
- **FR-009 to FR-010**: Verify response quality and logging functionality
- **FR-011 to FR-013**: Test AI integration and error handling
- **FR-014**: Authentication flow validation

### MCP Tool Validation
- Test each MCP tool individually for correct parameter handling
- Validate tool responses and error conditions
- Verify database consistency after tool operations

### Success Criteria Validation
- **SC-001**: Test natural language command accuracy (>90%)
- **SC-002**: Verify 100% of task operations use MCP tools
- **SC-003**: Test conversation history persistence (99.9% reliability)
- **SC-004**: Validate friendly response generation (100% compliance)
- **SC-005**: Test horizontal scaling and stateless operation
- **SC-006**: Verify logging of all tool invocations and errors
- **SC-008**: Test server restart resilience with no data loss

## 6. Constraints & Guardrails

### Technical Constraints
- **No Manual Coding**: All implementation via Claude Code only
- **Gemini API Routing**: All AI calls through configured base_url
- **MCP-Only Mutations**: Task operations exclusively via MCP tools
- **Stateless Backend**: All state persisted in database only

### Quality Constraints
- **Authentication Required**: All endpoints require JWT authentication
- **User Isolation**: Strict data separation between users
- **Character Limits**: 500 chars for input/output validation
- **Performance**: <500ms response time for AI interactions

## Outcome

- ✅ Impact: Complete implementation plan created with all required sections
- 🧪 Tests: Constitution checks passed and all requirements mapped
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/ created
- 🔁 Next prompts: Ready for /sp.tasks to break plan into executable tasks
- 🧠 Reflection: Plan is comprehensive and aligned with functional requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All constitution gates PASSED
- Prompt variant (if applicable): Standard /sp.plan workflow
- Next experiment (smallest change to try): Execute /sp.tasks to generate tasks.md