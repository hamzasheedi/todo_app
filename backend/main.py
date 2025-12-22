from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Handle both direct run and module run
try:
    from .routes import auth, tasks
    from .database import create_db_and_tables
except ImportError:
    try:
        from routes import auth, tasks
        from database import create_db_and_tables
    except ImportError:
        # For test environments, import directly
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from routes import auth, tasks
        from database import create_db_and_tables

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Todo API",
    description="API for the multi-user todo application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],  # Allow frontend and backend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose headers that browsers are allowed to access
    expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials"]
)

@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    try:
        from .database.migrations import run_migrations
        run_migrations()
    except ImportError:
        # Fallback to direct table creation if migrations module not available
        create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Todo API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Include routes
app.include_router(auth.router)
app.include_router(tasks.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)