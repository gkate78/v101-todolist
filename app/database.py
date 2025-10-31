"""
Database Configuration Module

This module sets up the database connection and session management.
We use SQLite (a file-based database) for simplicity, which is perfect for learning.

Key concepts:
- SQLAlchemy: An ORM (Object-Relational Mapping) tool that lets us interact with 
              the database using Python objects instead of writing raw SQL
- AsyncSession: An asynchronous database session that doesn't block the application
                while waiting for database operations
- Connection Pooling: Reuses database connections for better performance
"""

import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel

# Database URL - SQLite is a file-based database
# In production (Fly.io), use the volume mount path /app/data
# In development, use the local ./database.db
# This ensures data persists across deployments in production
DATABASE_DIR = os.getenv("DATABASE_DIR", "./")
DATABASE_FILE = os.path.join(DATABASE_DIR, "database.db")
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_FILE}"

# Create the database engine
# This is like opening a connection to the database
# echo=True means SQLAlchemy will print all SQL queries (great for debugging!)
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory
# A session is like a conversation with the database
# We create a new session for each request to ensure data consistency
AsyncSessionLocal = async_sessionmaker(
    engine,  # Use our database engine
    class_=AsyncSession,  # Use async sessions
    expire_on_commit=False  # Keep objects accessible after commit
)


async def get_db() -> AsyncSession:
    """
    Dependency function for FastAPI to get a database session.
    
    This is called automatically by FastAPI when a route needs database access.
    The 'yield' keyword makes this a generator function, which allows FastAPI
    to automatically close the session when the request is done.
    
    Usage in routes:
        async def my_route(db: AsyncSession = Depends(get_db)):
            # Use db here to query the database
    """
    async with AsyncSessionLocal() as session:
        # Yield the session to the route handler
        yield session
        # After the route completes, the session is automatically closed


async def init_db() -> None:
    """
    Initialize the database by creating all tables.
    
    This function reads all our SQLModel classes (like Todo) and creates
    the corresponding database tables. It's called once when the app starts.
    
    Think of this as creating the structure of your database before you start
    storing data in it.
    """
    async with engine.begin() as conn:
        # Create all tables defined in our models
        # run_sync is needed because SQLModel metadata operations are synchronous
        await conn.run_sync(SQLModel.metadata.create_all)

