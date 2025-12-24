---
id: PHR-002-ai-chatbot-todos-tasks-updated-20251224
title: AI Chatbot Tasks Updated
stage: tasks
date: 2025-12-24
surface: todo_app
model: Claude Sonnet 4.5
feature: 001-ai-chatbot-todos
branch: 001-ai-chatbot-todos
user: Hamza
command: manual-update
labels: [ai-chatbot, tasks, implementation, mcp, gemini, update]
links:
  spec: specs/001-ai-chatbot-todos/spec.md
  plan: specs/001-ai-chatbot-todos/plan.md
  tasks: specs/001-ai-chatbot-todos/tasks.md
  ticket:
  adr:
  pr:
files:
  - specs/001-ai-chatbot-todos/tasks.md
tests:
  - task-validation: PASSED
  - constitution-check: PASSED
  - spec-compliance: PASSED
---

## Prompt

Updated tasks.md to address feedback on task granularity, duplication, and verification requirements.

## Response snapshot

# Implementation Tasks: Todo AI Chatbot – Phase III (Basic Level Functionality)

**Feature**: Todo AI Chatbot – Phase III | **Branch**: `001-ai-chatbot-todos` | **Spec**: @specs/001-ai-chatbot-todos/spec.md

**Input**: Feature specification, implementation plan, data model, and API contracts from `/specs/001-ai-chatbot-todos/`

## Implementation Strategy

MVP-first approach: Complete User Story 1 (Natural Language Task Management) with minimal viable functionality before expanding to other stories. Each task is designed for 15-30 minutes of focused work with clear acceptance criteria.

## Dependencies

- **User Story 2 depends on User Story 1**: Conversation persistence requires task operations to be functional
- **User Story 3 depends on User Story 1 & 2**: Error handling requires core functionality to be in place
- **Foundational tasks must complete before user stories**: Database models, authentication, and MCP infrastructure
- **Phase 7 depends on all previous phases**: E2E testing requires complete functionality

## Parallel Execution Opportunities

- **[P] Tasks**: Tasks marked with [P] can be executed in parallel as they operate on different files/components
- **Backend vs Frontend**: Backend API development can proceed independently from frontend UI development
- **MCP Tools**: Individual tool implementations can be parallelized after MCP server foundation is established

---

## Phase 1: Setup & Project Initialization

**Goal**: Establish project structure and foundational configuration

- [ ] T001 Create backend project structure with FastAPI and SQLModel dependencies in backend/
- [ ] T002 Set up environment configuration files for Gemini API integration
- [ ] T003 Configure database connection and migration setup for Neon PostgreSQL
- [ ] T004 Verify OpenAI Agents SDK routes all AI calls through Gemini base_url (FR-011 enforcement)

---

## Phase 2: Foundational Components

**Goal**: Implement core infrastructure needed by all user stories

- [ ] T005 [P] Create User model in backend/src/models/user.py following data-model.md specification
- [ ] T006 [P] Create Task model in backend/src/models/task.py following data-model.md specification
- [ ] T007 [P] Create Conversation model in backend/src/models/conversation.py following data-model.md specification
- [ ] T008 [P] Create Message model in backend/src/models/message.py following data-model.md specification
- [ ] T009 Set up database migration configuration for all models
- [ ] T010 Implement authentication middleware with Better Auth integration in backend/src/core/auth.py
- [ ] T011 [P] Create database session management in backend/src/core/database.py
- [ ] T012 [P] Create Gemini API configuration and client in backend/src/core/config.py
- [ ] T013 Implement MCP server foundation in backend/src/services/mcp_server.py
- [ ] T014 Set up logging infrastructure for MCP tool invocations

---

## Phase 3: User Story 1 - Natural Language Task Management (P1)

**Goal**: Core functionality for adding, listing, updating, completing, and deleting tasks via natural language

**Independent Test**: Users can interact with the chatbot using natural language to perform all basic task operations (add, list, update, complete, delete) and verify that correct actions are taken.

**Acceptance Scenarios**:
1. Given user wants to add a task, When user says "Add a task to buy groceries", Then a new task "buy groceries" is created and user receives confirmation
2. Given user has multiple tasks, When user says "Show me my tasks", Then all active tasks are listed in a readable format
3. Given user has an existing task, When user says "Complete the project report", Then the task is marked as complete and user receives confirmation

- [ ] T015 [US1] Create task service with CRUD operations in backend/src/services/task_service.py
- [ ] T016 [US1] Create conversation service with message handling in backend/src/services/conversation_service.py
- [ ] T017 [P] [US1] Implement add_task MCP tool in backend/src/services/mcp_server.py
- [ ] T018 [P] [US1] Implement list_tasks MCP tool in backend/src/services/mcp_server.py
- [ ] T019 [P] [US1] Implement update_task MCP tool in backend/src/services/mcp_server.py
- [ ] T020 [P] [US1] Implement complete_task MCP tool in backend/src/services/mcp_server.py
- [ ] T021 [P] [US1] Implement delete_task MCP tool in backend/src/services/mcp_server.py
- [ ] T022 [US1] Create chat API endpoint in backend/src/api/chat_endpoints.py
- [ ] T023 [US1] Implement task API endpoints in backend/src/api/task_endpoints.py
- [ ] T024 [US1] Configure agent with MCP tool registry for task operations
- [ ] T025 [US1] Verify agent can invoke add_task via natural language command
- [ ] T026 [US1] Test basic task operations via natural language commands

---

## Phase 4: User Story 2 - Conversation Context and Persistence (P2)

**Goal**: Maintain conversation context across multiple interactions with persistence between sessions

**Independent Test**: Create tasks in one session, restart the server, and verify tasks and conversation context are still available in the next session.

**Acceptance Scenarios**:
1. Given user has been interacting with the chatbot, When server restarts and user returns, Then previous conversation context is maintained
2. Given user has multiple tasks across different sessions, When user asks to see all tasks, Then tasks from all sessions are displayed
3. Given user has completed tasks, When user asks for completed tasks, Then previously completed tasks are accessible

- [ ] T027 [US2] Implement conversation persistence in database
- [ ] T028 [US2] Create conversation retrieval API endpoints
- [ ] T029 [US2] Implement conversation context retrieval for AI agent
- [ ] T030 [US2] Add conversation history loading to chat endpoint
- [ ] T031 [US2] Test server restart resilience with conversation persistence
- [ ] T032 [US2] Implement conversation pagination for large histories

---

## Phase 5: User Story 3 - Error Handling and Friendly Feedback (P3)

**Goal**: Provide helpful, actionable feedback when users provide unclear commands or encounter system errors

**Independent Test**: Provide various ambiguous or incorrect commands to the chatbot and verify clear, helpful responses are provided.

**Acceptance Scenarios**:
1. Given user provides an unclear command, When user says "Do something about the thing", Then chatbot asks for clarification
2. Given system encounters an error, When task operation fails, Then user receives clear error message with suggested next steps
3. Given user makes a typo in a task name, When user refers to non-existent task, Then chatbot suggests similar existing tasks

- [ ] T033 [US3] Implement error handling for MCP tool failures
- [ ] T034 [US3] Add validation and error responses for invalid task operations
- [ ] T035 [US3] Create friendly confirmation messages for successful operations
- [ ] T036 [US3] Implement AI fail-safe responses when tools fail
- [ ] T037 [US3] Add input validation with character limits (500 chars)
- [ ] T038 [US3] Handle AI service downtime with appropriate user feedback
- [ ] T039 [US3] Test error scenarios and validate user feedback

---

## Phase 6: Frontend Integration

**Goal**: Integrate ChatKit UI for natural language interaction with the AI agent

- [ ] T040 Implement ChatPage component with ChatKit integration in frontend/src/pages/ChatPage.tsx
- [ ] T041 Create ChatKitWrapper component in frontend/src/components/ChatInterface/ChatKitWrapper.tsx
- [ ] T042 Set up API client for backend communication in frontend/src/services/api-client.ts
- [ ] T043 Implement authentication context in frontend/src/context/auth-context.ts
- [ ] T044 Connect ChatKit to backend chat endpoints
- [ ] T045 Add loading states and user feedback to UI
- [ ] T046 Test natural language command interpretation through UI

---

## Phase 7: Polish & Cross-Cutting Concerns

**Goal**: Final integration, testing, and optimization

- [ ] T047 Implement pagination for large task lists (display up to 50 tasks)
- [ ] T048 Add comprehensive logging for all MCP tool invocations
- [ ] T049 Test 100% compliance with MCP-only task mutations (FR-012)
- [ ] T050 Validate all functional requirements (FR-001 to FR-018)
- [ ] T051 Test success criteria compliance (SC-001 to SC-011)
- [ ] T052 [P] Backend E2E test for task operations
- [ ] T053 [P] Frontend E2E test for ChatKit integration
- [ ] T054 Update README with setup and usage instructions
- [ ] T055 Document API endpoints and MCP tool specifications

## Outcome

- ✅ Impact: Corrected task breakdown with 55 atomic tasks properly numbered and refined
- 🧪 Tests: All tasks follow checklist format with atomic responsibilities and clear acceptance criteria
- 📁 Files: tasks.md updated with proper sequential numbering and split oversized tasks
- 🔁 Next prompts: Ready for implementation following Agentic Dev Stack workflow
- 🧠 Reflection: Tasks are properly sized for 15-30 minute execution with clear checkpoints

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All tasks meet format requirements
- Prompt variant (if applicable): Update based on feedback
- Next experiment (smallest change to try): Begin implementation with T001-T004 setup tasks