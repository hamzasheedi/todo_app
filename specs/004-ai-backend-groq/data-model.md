# Data Model: AI Backend Updates with Groq Adoption

**Feature**: AI Backend Updates with Groq Adoption
**Spec ID**: 004-ai-backend-groq
**Created**: 2026-01-31

## Entities

### AIConfiguration
Represents the configuration for AI provider selection, including base_url, API key, and provider type

- **provider_type** (string): The type of AI provider (e.g., "groq", "openai", "openrouter", "cohere")
- **base_url** (string): The base URL for the AI provider API
- **api_key** (string): The API key for authenticating with the provider
- **model_name** (string): The specific model to use (e.g., "llama3-70b-8192")
- **timeout** (integer): Request timeout in seconds
- **fallback_enabled** (boolean): Whether fallback providers are enabled
- **fallback_base_url** (string, optional): Base URL for fallback provider
- **fallback_api_key** (string, optional): API key for fallback provider

### Conversation
Represents a user's conversation with the AI, persisted in the database to maintain context across requests

- **id** (UUID): Unique identifier for the conversation
- **title** (string, optional): Title of the conversation
- **user_id** (UUID): Foreign key to the user who owns this conversation
- **created_at** (datetime): Timestamp when the conversation was created
- **updated_at** (datetime): Timestamp when the conversation was last updated
- **messages** (JSON): Array of messages in the conversation
- **metadata** (JSON, optional): Additional metadata about the conversation

### MCPToolInvocation
Represents a call to an MCP tool, including parameters and authentication context

- **id** (UUID): Unique identifier for the tool invocation
- **tool_name** (string): Name of the MCP tool being invoked (e.g., "add_task", "list_tasks")
- **parameters** (JSON): Parameters passed to the tool
- **conversation_id** (UUID): Foreign key to the conversation that triggered this invocation
- **user_id** (UUID): Foreign key to the user who initiated the request
- **timestamp** (datetime): When the tool was invoked
- **status** (string): Status of the invocation ("pending", "success", "failed")
- **result** (JSON, optional): Result returned by the tool
- **error_message** (string, optional): Error message if the invocation failed