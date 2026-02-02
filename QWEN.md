# Todo AI Chatbot - Project Context

## Project Overview

The Todo AI Chatbot is a full-stack web application that enables users to manage their tasks using natural language commands through an AI-powered chatbot interface. The application consists of a Python/FastAPI backend with SQLModel ORM and a React/Next.js frontend.

### Key Features
- AI-powered chatbot that understands natural language commands for task management
- Add, list, update, complete, and delete tasks using conversational language
- Maintain conversation context across multiple interactions
- Persistent storage of tasks and conversation history in database
- Stateless backend architecture with database persistence
- MCP (Model Context Protocol) server for secure task operations
- Frontend integration with ChatKit UI
- Authentication and user isolation

### Architecture
- **Backend**: FastAPI with SQLModel ORM, PostgreSQL (Neon), JWT authentication
- **Frontend**: Next.js 16+, React, Tailwind CSS
- **AI Integration**: OpenAI Agents SDK configured with Google Gemini API
- **MCP Server**: Model Context Protocol server for secure task operations

## Building and Running

### Prerequisites
- Python 3.8+
- Node.js 18+ and npm
- pip (Python package installer)
- Git

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

### Environment Configuration
```bash
# From project root
cp .env.example .env
# Edit .env with your configuration including:
# - GEMINI_API_KEY: Your Google Gemini API key
# - GEMINI_BASE_URL: Gemini API base URL
# - OPENAI_API_KEY: Your Google Gemini API key (for compatibility)
# - OPENAI_BASE_URL: Gemini API base URL (for compatibility)
# - Database URL
```

### Database Setup
```bash
# From backend directory
alembic upgrade head
```

### Starting the Application
1. **Start the Backend Server:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   
   Or alternatively:
   ```bash
   python run_app.py
   # or
   python start_app.py
   ```

2. **Start the Frontend Development Server:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the Application:**
   - Backend API: `http://localhost:8000`
   - Frontend UI: `http://localhost:3000`
   - Chat Interface: `http://localhost:3000/chat`

## API Endpoints

### Backend API (http://localhost:8000)

**Core API (v1):**
- `POST /api/v1/chat/` - Chat endpoint for natural language task management
- `GET /api/v1/conversations/` - List user's conversations
- `GET /api/v1/conversations/{conversation_id}` - Get conversation history
- `POST /api/v1/tasks/` - Create a new task
- `GET /api/v1/tasks/` - List tasks with pagination
- `GET /api/v1/tasks/{task_id}` - Get a specific task
- `PUT /api/v1/tasks/{task_id}` - Update a specific task
- `DELETE /api/v1/tasks/{task_id}` - Delete a specific task

### MCP Server
- All task operations are executed exclusively via MCP tools
- Tools: add_task, list_tasks, update_task, complete_task, delete_task
- All tools require authentication and user context

## Data Models

### User Model
- `id`: UUID primary key
- `email`: Unique email address
- `better_auth_id`: Optional Better Auth ID
- `created_at`: Timestamp
- `updated_at`: Timestamp
- Relationships: tasks, conversations

### Task Model
- `id`: UUID primary key
- `title`: Task title (1-200 chars)
- `description`: Optional description (up to 500 chars)
- `status`: Task status ("incomplete" or "complete")
- `user_id`: Foreign key to user
- `created_date`: Creation timestamp
- `updated_date`: Update timestamp
- Relationship: user

### Conversation Model
- `id`: UUID primary key
- `title`: Optional conversation title (up to 200 chars)
- `user_id`: Foreign key to user
- `created_at`: Creation timestamp
- `updated_at`: Update timestamp
- Relationships: user, messages

### Message Model
- `id`: UUID primary key
- `content`: Message content (1-2000 chars)
- `role`: Message role ("user" or "assistant")
- `conversation_id`: Foreign key to conversation
- `user_id`: Foreign key to user
- `timestamp`: Message timestamp
- Relationships: conversation, user

## Development Conventions

### Backend
- All state is persisted in the database; no in-memory state
- All task mutations happen through MCP tools
- All AI logic routes through OpenAI Agents SDK via Gemini API
- Strict data separation between users
- Task lists limited to 50 items with pagination controls
- All user input limited to 500 characters

### Frontend
- Next.js 16+ with App Router
- Tailwind CSS for styling
- React Context API for state management
- Custom API client with authentication handling

## Testing

### Backend Tests
```bash
cd backend
python -m pytest
```

### Database Migrations
```bash
cd backend
alembic revision --autogenerate -m "Migration message"
alembic upgrade head
```

## Key Components

### AI Agent Service
Located at `backend/services/ai_agent.py`, this service uses the OpenAI SDK configured with Google Gemini API to process natural language and invoke MCP tools. It handles the conversation flow and tool execution.

### MCP Server
Located at `backend/services/mcp_server.py`, this implements the Model Context Protocol server with tools for task operations (add, list, update, complete, delete). All task mutations happen through these secure tools.

### Authentication
JWT-based authentication with user isolation. Located in `backend/auth/` directory.

### Database Layer
SQLModel ORM with PostgreSQL database. Located in `backend/database/` directory with Alembic migrations.

## Constraints & Architecture Decisions

1. **Stateless Backend**: All state is persisted in the database; no in-memory state
2. **MCP-Only Operations**: All task mutations happen through MCP tools
3. **AI Routing**: All AI logic routes through OpenAI Agents SDK via Gemini API
4. **User Isolation**: Strict data separation between users
5. **Pagination**: Task lists limited to 50 items with pagination controls
6. **Input Validation**: All user input limited to 500 characters
