#!/usr/bin/env python3
"""
Script to add the missing better_auth_id column to the user table
This addresses the schema mismatch where the User model expects better_auth_id
but the database doesn't have this column.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create the engine with proper settings for Neon PostgreSQL
if DATABASE_URL.startswith("postgresql"):
    # For PostgreSQL, we need to handle SSL properly
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,      # fixes dead SSL connections
        pool_recycle=300,        # prevents Neon from closing idle connections
        pool_size=20,            # number of connections to maintain
        max_overflow=0,          # additional connections beyond pool_size
        pool_timeout=30,         # seconds to wait before giving up on a connection
    )
else:
    # For SQLite and other databases
    engine = create_engine(DATABASE_URL)

def add_better_auth_id_column():
    """Add the better_auth_id column to the user table if it doesn't exist"""
    with engine.connect() as conn:
        # Check if the column already exists
        if DATABASE_URL.startswith("postgresql"):
            # PostgreSQL query to check if column exists
            result = conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'user' AND column_name = 'better_auth_id'
            """))
        else:
            # For SQLite
            result = conn.execute(text("PRAGMA table_info(user)"))
            columns = [row[1] for row in result.fetchall()]  # column name is in index 1
            if 'better_auth_id' in columns:
                result = [('better_auth_id',)]  # Mock result to indicate column exists
            else:
                result = []  # Empty result to indicate column doesn't exist

        if result.fetchone():
            print("Column 'better_auth_id' already exists in user table")
            return True

        # Add the column
        try:
            if DATABASE_URL.startswith("postgresql"):
                # Add the column as optional (nullable) to avoid issues with existing rows
                alter_query = text("""
                    ALTER TABLE "user"
                    ADD COLUMN better_auth_id VARCHAR(255) UNIQUE
                """)
            else:
                # For SQLite (fallback)
                alter_query = text("ALTER TABLE user ADD COLUMN better_auth_id TEXT UNIQUE")

            conn.execute(alter_query)
            conn.commit()
            print("Successfully added 'better_auth_id' column to user table")
            return True
        except Exception as e:
            print(f"Error adding column: {e}")
            return False

if __name__ == "__main__":
    print("Adding better_auth_id column to user table...")
    success = add_better_auth_id_column()
    if success:
        print("Migration completed successfully!")
    else:
        print("Migration failed!")
        exit(1)