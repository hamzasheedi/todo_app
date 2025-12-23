from sqlmodel import create_engine, Session

# Handle relative imports for different execution contexts
try:
    from ..models import User, Task  # Import all models to register them
except ImportError:
    # Direct imports for test environments
    from models import User, Task

from dotenv import load_dotenv
import os

# Load environment variables - look in parent directory as well
load_dotenv()
load_dotenv(".env")  # Look for .env in current directory
load_dotenv("../.env")  # Look for .env in parent directory

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create the engine with appropriate settings for different databases
if DATABASE_URL.startswith("sqlite"):
    # For SQLite, we need to add connect_args={"check_same_thread": False}
    engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
else:
    # For PostgreSQL and other databases - add connection pooling for Neon
    engine = create_engine(
        DATABASE_URL,
        echo=True,
        pool_pre_ping=True,      # fixes dead SSL connections
        pool_recycle=300,        # prevents Neon from closing idle connections
        pool_size=20,            # number of connections to maintain
        max_overflow=0,          # additional connections beyond pool_size
        pool_timeout=30,         # seconds to wait before giving up on a connection
    )

def create_db_and_tables():
    """Create database tables for all models"""
    from sqlmodel import SQLModel

    # Handle relative imports for different execution contexts
    try:
        from ..models.user import User
        from ..models.task import Task
    except ImportError:
        # Direct imports for test environments
        from models.user import User
        from models.task import Task

    # Ensure all models are imported before creating tables
    # Create tables with the new schema (this should update the existing tables)
    # For production databases, consider using proper migrations instead
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get a database session"""
    with Session(engine) as session:
        yield session

# SessionLocal for dependency injection
def SessionLocal():
    with Session(engine) as session:
        yield session