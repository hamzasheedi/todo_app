from sqlmodel import create_engine, Session
from .models import User, Task  # Import all models to register them
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/todo_db")

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Create database tables for all models"""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get a database session"""
    with Session(engine) as session:
        yield session

# SessionLocal for dependency injection
from sqlmodel import Session
def SessionLocal():
    with Session(engine) as session:
        yield session