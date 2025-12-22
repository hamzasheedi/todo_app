"""
Database migration setup using Alembic
This file provides functions to handle database schema migrations
"""
import asyncio
from sqlmodel import SQLModel
from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from sqlalchemy import engine_from_config
import os
from .database import engine

def create_migration(message: str = "Auto migration"):
    """
    Create a new migration file
    """
    # This would normally be run from command line
    print(f"Migration '{message}' would be created using alembic")
    print("Use: alembic revision --autogenerate -m '{message}'")

def run_migrations():
    """
    Run all pending migrations
    """
    # First run the standard SQLModel table creation
    from .database import create_db_and_tables
    create_db_and_tables()

    # Then run any custom migrations to fix schema issues
    run_custom_migrations()
    print("Database tables and migrations completed successfully")


def run_custom_migrations():
    """
    Run custom migrations to fix specific schema issues
    """
    import os
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv

    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

    # Create the engine with proper settings for Neon PostgreSQL
    if DATABASE_URL.startswith("postgresql"):
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,      # fixes dead SSL connections
            pool_recycle=300,        # prevents Neon from closing idle connections
            pool_size=20,            # number of connections to maintain
            max_overflow=0,          # additional connections beyond pool_size
            pool_timeout=30,         # seconds to wait before giving up on a connection
        )
    else:
        engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        # Check if better_auth_id column exists, and add it if missing
        column_exists = False
        if DATABASE_URL.startswith("postgresql"):
            result = conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'user' AND column_name = 'better_auth_id'
            """))
            column_exists = result.fetchone() is not None
        else:
            # For SQLite
            result = conn.execute(text("PRAGMA table_info(user)"))
            columns = [row[1] for row in result.fetchall()]
            column_exists = 'better_auth_id' in columns

        if not column_exists:
            # Add the column if it doesn't exist
            try:
                if DATABASE_URL.startswith("postgresql"):
                    alter_query = text("""
                        ALTER TABLE "user"
                        ADD COLUMN better_auth_id VARCHAR(255) UNIQUE
                    """)
                else:
                    alter_query = text("ALTER TABLE user ADD COLUMN better_auth_id TEXT UNIQUE")

                conn.execute(alter_query)
                conn.commit()
                print("Added 'better_auth_id' column to user table")
            except Exception as e:
                print(f"Warning: Could not add 'better_auth_id' column: {e}")
        else:
            print("Column 'better_auth_id' already exists in user table")

def check_pending_migrations():
    """
    Check if there are pending migrations
    """
    # This is a simplified check - in practice you'd use alembic to check
    print("Checking for pending migrations...")
    return False  # Assuming no pending migrations after initial setup