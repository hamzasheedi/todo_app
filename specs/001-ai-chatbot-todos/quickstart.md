# Quickstart Guide: Todo AI Chatbot – Phase III

## Prerequisites
- Python 3.13+
- Node.js 18+ (for frontend)
- Neon PostgreSQL account
- Gemini API key
- Better Auth configuration

## Setup Instructions

### 1. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Update .env with your configuration:
# - GEMINI_API_KEY: Your Gemini API key
# - DATABASE_URL: Neon PostgreSQL connection string
# - BETTER_AUTH_SECRET: Secret for JWT signing
# - NEXTAUTH_URL: Your application URL
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python -m src.core.migrate

# Start the backend server
python -m src.main
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

### 4. MCP Server Configuration
```bash
# The MCP server will be started automatically with the backend
# It exposes task operations as tools for the AI agent
```

## API Endpoints

### Chat Endpoints
- `POST /api/chat` - Send message to AI agent
- `GET /api/conversations` - List user conversations
- `GET /api/conversations/{id}` - Get specific conversation
- `GET /api/messages/{conversation_id}` - Get messages for conversation

### Task Endpoints
- `GET /api/tasks` - List user tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/complete` - Mark task as complete

## MCP Tools Available

### Task Management Tools
- `add_task` - Create a new task
- `list_tasks` - Retrieve all user tasks
- `update_task` - Modify an existing task
- `complete_task` - Mark a task as completed
- `delete_task` - Remove a task

## Authentication
All API endpoints require JWT authentication via Better Auth. The frontend handles token acquisition and includes it in all requests automatically.

## Natural Language Examples
- "Add a task to buy groceries" - Creates a new task
- "Show me my tasks" - Lists all current tasks
- "Mark the project report as done" - Completes a task
- "Delete the meeting note task" - Removes a task
- "Update the deadline for the presentation" - Modifies a task

## Development
```bash
# Run backend tests
cd backend && pytest

# Run frontend tests
cd frontend && npm test

# Check backend code formatting
cd backend && black . && flake8 .

# Check frontend code formatting
cd frontend && npm run lint && npm run format
```