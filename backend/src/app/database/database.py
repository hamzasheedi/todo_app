from sqlmodel import create_engine, Session

from dotenv import load_dotenv
import os

# Load environment variables - look in parent directory as well
load_dotenv()
load_dotenv(".env")  # Look for .env in current directory
load_dotenv("../.env")  # Look for .env in parent directory

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
print(f"Database URL: {DATABASE_URL}")

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

    # Import the models initialization to register them once
    from app.models.init_models import initialize_models
    initialize_models()

    # Create tables with the new schema (this should update the existing tables)
    # For production databases, consider using proper migrations instead
    try:
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Warning: Could not create database tables: {e}")
        # Continue execution even if table creation fails

def get_session():
    """Get a database session"""
    with Session(engine) as session:
        yield session

# SessionLocal for dependency injection
def SessionLocal():
    with Session(engine) as session:
        yield session