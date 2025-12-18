# Quickstart Guide: Phase II Multi-User Todo Application

## Project Setup

### Prerequisites
- Node.js 18+ for Next.js frontend
- Python 3.13+ for FastAPI backend
- PostgreSQL-compatible database (Neon Serverless PostgreSQL)
- Git for version control

### Environment Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Install frontend dependencies**:
   ```bash
   cd frontend  # or wherever Next.js app is located
   npm install
   ```

3. **Install backend dependencies**:
   ```bash
   cd backend  # or wherever FastAPI app is located
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file with the following variables:
   ```env
   DATABASE_URL="postgresql://username:password@host:port/database"
   AUTH_SECRET="your-secure-auth-secret"
   NEXTAUTH_URL="http://localhost:3000"
   JWT_SECRET="your-jwt-secret-key"
   ```

## Architecture Overview

### Technology Stack
- **Frontend**: Next.js 16+ with App Router, TypeScript, Tailwind CSS
- **Backend**: FastAPI with SQLModel ORM
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens
- **API**: Stateless REST under `/api/` with consistent HTTP status codes

### Project Structure
```
project/
├── frontend/                 # Next.js application
│   ├── app/                  # App Router pages
│   ├── components/           # React components
│   ├── lib/                  # Utility functions
│   └── package.json
├── backend/                  # FastAPI application
│   ├── main.py              # Application entry point
│   ├── auth/                # Authentication logic
│   ├── models/              # SQLModel database models
│   ├── routes/              # API route definitions
│   └── requirements.txt
├── specs/                   # Project specifications
│   └── 003-multi-user-todo/ # Current feature specs
├── docs/                    # Documentation
└── README.md
```

## Running the Application

### Development Mode

1. **Start the database** (if using local PostgreSQL):
   ```bash
   # Ensure PostgreSQL is running locally
   # Or connect to Neon PostgreSQL instance
   ```

2. **Start the backend**:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

3. **Start the frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/
   - API Documentation: http://localhost:8000/docs

## Key Features

### Authentication
- User registration and login via Better Auth
- JWT token-based authentication
- Automatic token refresh 5 minutes before expiration
- Secure session management

### Task Management
- Create, read, update, delete tasks
- Mark tasks as complete/incomplete
- Sort tasks by various criteria (Newest First, Oldest First, etc.)
- User-specific task isolation

### Security
- JWT validation on every API request
- User ID verification in URL parameters
- Cross-user access prevention
- Input validation and sanitization

## API Endpoints

### Authentication (Better Auth)
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- `POST /api/auth/signout` - User logout

### Task Management
- `GET /api/{user_id}/tasks` - Get user's tasks with sorting options
- `POST /api/{user_id}/tasks` - Create new task for user
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update specific task
- `DELETE /api/{user_id}/tasks/{id}` - Delete specific task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Mark task as complete/incomplete

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Validation error
- `401` - Unauthenticated
- `403` - Unauthorized (cross-user access)
- `404` - Not found

## Configuration

### Environment Variables
- `DATABASE_URL` - Database connection string
- `AUTH_SECRET` - Better Auth secret key
- `NEXTAUTH_URL` - Application base URL
- `JWT_SECRET` - JWT signing secret (if needed beyond Better Auth)

### Database Migrations
The application uses SQLModel for database schema management. To create and run migrations:
```bash
# From backend directory
python -m scripts.create_db_and_tables  # Initial setup
# Or use Alembic for more complex migration management
```

## Testing

### Frontend Testing
```bash
cd frontend
npm run test
npm run test:watch  # For continuous testing
```

### Backend Testing
```bash
cd backend
python -m pytest
python -m pytest --cov  # For coverage report
```

## Deployment

### Frontend Deployment
1. Build the Next.js application: `npm run build`
2. Deploy to Vercel, Netlify, or other Next.js-compatible platform
3. Ensure environment variables are properly configured

### Backend Deployment
1. Deploy FastAPI application to hosting platform (Heroku, Railway, etc.)
2. Configure database connection and environment variables
3. Ensure proper SSL configuration for production

## Troubleshooting

### Common Issues
1. **Authentication not working**: Verify AUTH_SECRET and NEXTAUTH_URL are correctly set
2. **Database connection errors**: Check DATABASE_URL format and credentials
3. **Cross-user access**: Verify JWT validation and user_id matching are properly implemented
4. **CORS issues**: Ensure frontend and backend URLs are properly configured

### Development Tips
- Use the API documentation at `/docs` to test endpoints during development
- Check the browser's developer tools for authentication and API call issues
- Review server logs for backend errors
- Verify that all environment variables are properly set in both frontend and backend