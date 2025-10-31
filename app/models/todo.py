"""
Todo Model - Database Table Definition

This file defines the structure of our Todo table in the database.
Using SQLModel, we define the table structure using Python classes.

Key concepts:
- SQLModel: Combines SQLAlchemy (database ORM) with Pydantic (data validation)
- Table=True: Makes this class a database table (not just a data class)
- Field: Used to define columns with specific properties (primary_key, default, etc.)
- Optional: Indicates a field can be None (nullable in database terms)
"""

from typing import Optional
from sqlmodel import SQLModel, Field


class Todo(SQLModel, table=True):
    """
    Todo Model - Represents a single todo item in the database.
    
    This class defines:
    1. The database table structure (columns, types, constraints)
    2. How Python objects map to database rows
    
    Example:
        todo = Todo(title="Buy groceries", completed=False)
        # This creates a Python object that represents a database row
    """
    
    # Primary key - unique identifier for each todo
    # Optional[int] means it can be None initially (database will auto-generate it)
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Todo title - the text describing what needs to be done
    # This is required (not Optional), so every todo must have a title
    title: str = Field(max_length=200)  # Limit title to 200 characters
    
    # Completion status - whether the todo is done or not
    # Default to False (not completed) when a new todo is created
    completed: bool = Field(default=False)
    
    # Optional: You can add more fields later, like:
    # created_at: Optional[datetime] = Field(default_factory=datetime.now)
    # priority: Optional[int] = Field(default=1)

