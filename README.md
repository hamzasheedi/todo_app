# Todo AI Chatbot - Phase III (Basic Level Functionality)

An AI-powered chatbot interface for managing todos using natural language, built with Python, FastAPI, SQLModel, and React/Next.js.

## Features

- AI-powered chatbot that understands natural language commands
- Add, list, update, complete, and delete tasks using conversational language
- Maintain conversation context across multiple interactions
- Persistent storage of tasks and conversation history in database
- Stateless backend architecture with database persistence
- MCP (Model Context Protocol) server for task operations
- Frontend integration with ChatKit UI
- Authentication and user isolation

## Prerequisites

- Python 3.8 or higher
- Node.js 18+ and npm
- pip (Python package installer)
- Git

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd todo-app
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup:**
   ```bash
   cd frontend  # from project root
   npm install
   ```

4. **Environment Configuration:**
   ```bash
   # From project root
   cp .env.example .env
   # Edit .env with your configuration including:
   # - GROQ_API_KEY: Your Groq API key (primary provider)
   # - GROQ_BASE_URL: Groq API base URL (default: https://api.groq.com/openai/v1)
   # - OPENAI_API_KEY: Your OpenAI API key (fallback provider)
   # - OPENAI_BASE_URL: OpenAI API base URL (default: https://api.openai.com/v1)
   # - Database URL
   ```

5. **Database Setup:**
   ```bash
   # From backend directory
   alembic upgrade head
   ```

## Usage

1. **Start the Backend Server:**
   ```bash
   # From project root directory
   python start_backend.py
   ```

   OR, if running directly with uvicorn:
   ```bash
   # From project root directory
   uvicorn app.main:app --reload --app-dir src
   ```

   **Note**: The application uses a `src/app/` layout. When running uvicorn directly, ensure you use `--app-dir src` to correctly resolve imports from the `app` module.

2. **Start the Frontend Development Server:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the Application:**
   - Backend API: `http://localhost:8000`
   - Frontend UI: `http://localhost:3000`
   - Chat Interface: `http://localhost:3000/chat`

4. **Use the AI Chatbot:**
   - Navigate to the chat interface
   - Log in with your credentials
   - Use natural language commands like:
     - "Add a task to buy groceries"
     - "Show me my tasks"
     - "Complete the project report"
     - "Update my shopping task to include milk and bread"
     - "Delete the old task"

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

**Legacy API:**
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/tasks` - Get all tasks (legacy)
- `POST /api/tasks` - Create a new task (legacy)

### MCP Server
- All task operations are executed exclusively via MCP tools
- Tools: add_task, list_tasks, update_task, complete_task, delete_task
- All tools require authentication and user context

## Architecture

### Backend
- **Framework**: FastAPI
- **ORM**: SQLModel with PostgreSQL (Neon)
- **Authentication**: JWT-based with user isolation
- **AI Integration**: OpenAI Agents SDK configured with OpenAI-compatible API (Groq as primary provider)
- **MCP Server**: Model Context Protocol server for task operations
- **Database**: Neon Serverless PostgreSQL with Alembic migrations

### Frontend
- **Framework**: Next.js 16+ with App Router
- **UI**: Tailwind CSS with ChatKit integration
- **State Management**: React Context API
- **API Client**: Custom API client with authentication handling

## Configuration

### Environment Variables

**Backend (.env):**
- `GROQ_API_KEY` - Your Groq API key (primary provider)
- `GROQ_BASE_URL` - Groq API base URL (default: https://api.groq.com/openai/v1)
- `OPENAI_API_KEY` - Your OpenAI API key (fallback provider)
- `OPENAI_BASE_URL` - OpenAI API base URL (default: https://api.openai.com/v1)
- `DATABASE_URL` - Database connection string
- `AUTH_SECRET` - Secret for JWT authentication
- `JWT_SECRET` - Secret for JWT token signing
- `NEXTAUTH_URL` - Base URL for the application

### MCP Tool Configuration

All task operations are performed exclusively through MCP tools:
- `add_task`: Create new tasks with title and description
- `list_tasks`: Retrieve user's tasks with pagination support
- `update_task`: Modify existing tasks
- `complete_task`: Mark tasks as completed
- `delete_task`: Remove tasks

## Constraints & Architecture Decisions

1. **Stateless Backend**: All state is persisted in the database; no in-memory state
2. **MCP-Only Operations**: All task mutations happen through MCP tools
3. **AI Routing**: All AI logic routes through OpenAI Agents SDK via OpenAI-compatible API (provider-agnostic)
4. **User Isolation**: Strict data separation between users
5. **Pagination**: Task lists limited to 50 items with pagination controls
6. **Input Validation**: All user input limited to 500 characters

## Running Tests

To run backend tests:
```bash
cd backend
python -m pytest
```

## Database Migrations

To run database migrations:
```bash
cd backend
alembic revision --autogenerate -m "Migration message"
alembic upgrade head
```

## Deployment

The application supports independent frontend and backend deployment:
- Backend: Deploy to any Python-compatible hosting (Heroku, AWS, GCP, etc.)
- Frontend: Deploy to Vercel, Netlify, or any static hosting service

## License

MIT License