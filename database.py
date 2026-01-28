# Database Configuration for Smart Energy Platform
# This file handles all PostgreSQL database connections and setup

# Import SQLAlchemy components for database operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
import os

# ============================================================================
# Database Configuration
# ============================================================================
# PostgreSQL connection string format:
# postgresql://username:password@host:port/database_name
# 
# Example for local development:
# DATABASE_URL = "postgresql://postgres:password@localhost:5432/smart_energy"
# 
# Make sure to replace with your actual database credentials

# Read from environment variable, fallback to local development URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/smart_energy"
)

# ============================================================================
# Create Database Engine
# ============================================================================
# The engine is the connection pool that manages database connections
# 
# Parameters:
# - echo=True: Print SQL queries to console (useful for debugging)
# - pool_pre_ping=True: Test connections before using them (ensures healthy connections)
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)

# ============================================================================
# Create Session Factory
# ============================================================================
# SessionLocal is used to create individual database sessions
# Each API request will have its own session for database operations
SessionLocal = sessionmaker(
    autocommit=False,  # Don't auto-commit changes
    autoflush=False,   # Don't auto-flush pending changes
    bind=engine        # Use the engine we created above
)

# ============================================================================
# Create Base Class for Models
# ============================================================================
# All database models (tables) must inherit from this Base class
# This allows SQLAlchemy to track and manage them
Base = declarative_base()

# ============================================================================
# Dependency Function for FastAPI
# ============================================================================
# This function provides a database session to API endpoints
# It automatically handles session cleanup after each request
def get_db():
    """
    Get a database session for API requests.
    
    This function creates a new database session for each API request
    and automatically closes it when the request is complete.
    
    Usage in FastAPI endpoints:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            # Your code here
            pass
    
    Yields:
        Session: A SQLAlchemy database session for database operations
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
