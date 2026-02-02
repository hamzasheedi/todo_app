# Quickstart Guide: AI Backend Updates with Groq Adoption

**Feature**: AI Backend Updates with Groq Adoption
**Spec ID**: 004-ai-backend-groq
**Created**: 2026-01-31

## Overview

This guide provides instructions for setting up and running the AI chatbot with Groq as the primary provider. The system maintains all existing functionality while improving performance and reliability through the new provider.

## Prerequisites

- Python 3.8+
- Node.js 18+ (for frontend, if applicable)
- Groq API key
- PostgreSQL database (or Neon Serverless PostgreSQL)

## Setup Steps

### 1. Environment Configuration

Set up the required environment variables:

```bash
# Primary AI provider (Groq)
export AI_PROVIDER=groq
export AI_BASE_URL=https://api.groq.com/openai/v1
export AI_API_KEY=your_groq_api_key_here
export AI_MODEL=llama3-70b-8192  # or another supported model

# Optional: Fallback provider
export FALLBACK_AI_BASE_URL=https://api.openai.com/v1
export FALLBACK_AI_API_KEY=your_openai_api_key_for_fallback

# Timeout settings
export AI_TIMEOUT=30

# Database configuration
export DATABASE_URL=postgresql://username:password@localhost/dbname

# Authentication
export AUTH_SECRET=your_auth_secret
export JWT_SECRET=your_jwt_secret
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Database Setup

```bash
cd backend
alembic upgrade head
```

### 4. Run the Application

```bash
cd backend
uvicorn main:app --reload
```

## Verification Steps

1. **Provider Configuration Test**:
   - Send a simple message to the chat endpoint
   - Verify that the response comes from the Groq-powered AI

2. **MCP Tool Integration Test**:
   - Issue a command that should trigger an MCP tool (e.g., "Add a task to buy groceries")
   - Verify that the appropriate MCP tool is called

3. **Fallback Mechanism Test**:
   - Temporarily disable the primary provider
   - Verify that the system attempts to use the fallback provider

4. **Stateless Operation Test**:
   - Restart the server
   - Verify that conversation history is preserved in the database

## Troubleshooting

### Common Issues

- **Invalid API Key**: Ensure your Groq API key is valid and has sufficient quota
- **Network Connectivity**: Verify that the application can reach the AI provider
- **MCP Tools Not Called**: Check that the AI agent is properly configured to use MCP tools

### Logs to Monitor

- AI provider interactions
- MCP tool invocations
- Error responses and fallback attempts
- Authentication and authorization events