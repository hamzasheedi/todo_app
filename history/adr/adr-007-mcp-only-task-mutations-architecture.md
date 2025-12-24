---
id: ADR-007
title: MCP-Only Task Mutations Architecture
date: 2025-12-24
status: Accepted
area: System Architecture
---

## Context

The system must ensure that all task operations (add, list, update, complete, delete) are performed exclusively through MCP tools, as specified in functional requirement FR-012. This creates a clear separation between AI intent recognition and actual task operations, with the AI agent determining which tools to invoke based on user input.

## Decision

All task mutations will be performed exclusively via MCP (Model Context Protocol) tools. The AI agent will process natural language input, determine the appropriate MCP tool to invoke, and the MCP server will execute the actual database operations. This creates a clear boundary where the AI agent handles intent recognition and response generation, while MCP tools handle the actual data operations.

## Alternatives Considered

1. **Direct API calls from AI agent**: Allow the AI agent to make direct API calls to backend endpoints for task operations
   - Rejected because it violates FR-012 requirement for MCP-only task mutations
   - Would create tight coupling between AI logic and backend implementation

2. **Hybrid approach**: Some operations via MCP tools, others via direct API calls
   - Rejected because it would not maintain consistency and violate the requirement for exclusive MCP tool usage

3. **Custom tool framework**: Build a custom tool framework instead of using MCP
   - Rejected because MCP is the standard protocol and provides better integration with AI agents

## Consequences

### Positive
- Complies with functional requirement FR-012 (MCP-only task mutations)
- Provides clear separation of concerns between AI processing and data operations
- Enables better logging and monitoring of tool invocations (FR-010)
- Supports extensibility by allowing new tools to be added without changing AI logic

### Negative
- Adds complexity with additional tool layer and routing
- May introduce slight latency due to tool invocation overhead
- Requires more sophisticated error handling between AI agent and tools

## Scope Impact

- AI Agent: Must be configured to recognize when to invoke MCP tools
- MCP Server: Must implement all required task operation tools
- Backend: API endpoints will coordinate with MCP tools
- Data Layer: MCP tools will handle all database operations
- Testing: Tool invocation and responses need to be validated

## References

- Feature specification: `/specs/001-ai-chatbot-todos/spec.md` (FR-012)
- Implementation plan: `/specs/001-ai-chatbot-todos/plan.md`
- Data model: `/specs/001-ai-chatbot-todos/data-model.md`