# Research Summary: Todo AI Chatbot – Phase III

## Decision: MCP Tool Specifications for Task Operations
**Rationale**: MCP tools are required as per functional requirement FR-012 to execute all task operations exclusively via MCP tools. This ensures a clean separation between AI intent recognition and actual task operations.

**Alternatives considered**:
- Direct API calls from AI agent: Would violate FR-012 requirement for MCP-only task mutations
- Hybrid approach: Would complicate architecture and violate stateless constraint

## Decision: Gemini API Integration via OpenAI SDK
**Rationale**: As specified in FR-011, all AI logic must be routed through OpenAI Agents SDK via Gemini API. This provides consistency and leverages existing AI infrastructure.

**Alternatives considered**:
- Direct OpenAI API calls: Would not meet the Gemini API routing requirement
- Multiple AI provider support: Would add unnecessary complexity for Phase III

## Decision: Stateless Backend with Database Persistence
**Rationale**: Constitution principle XIII requires conversation state to be persisted to database with server holding no in-memory state. This enables horizontal scaling and resilience to server restarts.

**Alternatives considered**:
- In-memory state: Would violate stateless architecture requirement
- Redis caching: Would add complexity without clear benefit for Phase III

## Decision: ChatKit UI for Frontend
**Rationale**: Feature specification requires OpenAI Agents SDK ChatKit UI for user interaction. This provides a ready-made, tested interface for AI chat interactions.

**Alternatives considered**:
- Custom chat interface: Would require significant additional development time
- Alternative chat libraries: Would not align with OpenAI Agents SDK requirement

## Decision: Neon PostgreSQL for Data Storage
**Rationale**: Feature specification requires Neon Serverless PostgreSQL for storing tasks, conversations, and messages. This provides serverless scalability and aligns with existing project architecture.

**Alternatives considered**:
- SQLite: Would not meet serverless requirement for production deployment
- MongoDB: Would not align with existing SQLModel-based architecture

## Decision: Better Auth for Authentication
**Rationale**: Constitution principle IX requires authentication for all data access with user isolation. Better Auth provides JWT-based authentication that integrates well with FastAPI.

**Alternatives considered**:
- Custom authentication: Would require additional development and security considerations
- OAuth providers only: Would not provide simple authentication option for development