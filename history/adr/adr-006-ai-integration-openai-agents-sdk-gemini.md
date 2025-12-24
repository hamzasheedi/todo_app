---
id: ADR-006
title: AI Integration via OpenAI Agents SDK with Gemini API
date: 2025-12-24
status: Accepted
area: AI Integration
---

## Context

The system needs to integrate AI capabilities for natural language processing of todo management commands. The specification requires using the OpenAI Agents SDK via Gemini API with a configured base_url, rather than direct OpenAI API calls. This affects how AI logic is routed, processed, and executed.

## Decision

We will integrate the OpenAI Agents SDK configured with a Gemini-compatible base_url and API key to handle natural language processing for todo management. All AI logic will be routed through this SDK, with the Gemini API serving as the underlying AI provider.

## Alternatives Considered

1. **Direct OpenAI API calls**: Make direct calls to OpenAI's API endpoints without using the Agents SDK
   - Rejected because it would not comply with the requirement to route all AI logic through the OpenAI Agents SDK via Gemini API

2. **Multiple AI provider support**: Implement abstraction layer to support OpenAI, Gemini, and other providers simultaneously
   - Rejected because it adds unnecessary complexity for Phase III requirements

3. **Custom NLP processing**: Build custom natural language processing instead of using AI services
   - Rejected because it would require significant development time and expertise

## Consequences

### Positive
- Complies with functional requirement FR-011 (AI routing through OpenAI Agents SDK via Gemini API)
- Leverages existing AI infrastructure and capabilities
- Provides consistent AI interaction patterns

### Negative
- Creates dependency on Gemini API availability and rate limits
- May have different performance characteristics than direct OpenAI API
- Adds complexity due to SDK integration requirements

## Scope Impact

- Frontend: ChatKit UI will interact with the AI agent
- Backend: API endpoints will route messages to the AI agent
- MCP Server: AI agent will determine when to invoke MCP tools
- Infrastructure: Requires proper API key management and base_url configuration

## References

- Feature specification: `/specs/001-ai-chatbot-todos/spec.md` (FR-011)
- Implementation plan: `/specs/001-ai-chatbot-todos/plan.md`