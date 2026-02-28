"""
Todo Controller - Business Logic Layer

This module contains the business logic for todo operations.
Controllers handle the actual work: creating, reading, updating, and deleting todos.

Why separate controllers from routes?
- Routes handle HTTP requests/responses (the "how" of communication)
- Controllers handle business logic (the "what" we're actually doing)
- This separation makes code easier to test and maintain

CRUD Operations:
- Create: Add a new todo
- Read: Get todos (all or one by ID)
- Update: Modify an existing todo
- Delete: Remove a todo
"""

from datetime import date
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException

from app.models.todo import Todo


def calculate_priority_from_due_date(due_date: Optional[date]) -> int:
    """
    Calculate priority from due date.

    Rules:
    - Due today/tomorrow or overdue -> High (3)
    - Due within a week -> Medium (2)
    - Due later than a week -> Low (1)
    - No due date -> Medium (2)
    """
    if due_date is None:
        return 2

    days_until_due = (due_date - date.today()).days
    if days_until_due <= 1:
        return 3
    if days_until_due <= 7:
        return 2
    return 1


async def create_todo(
    db: AsyncSession,
    title: str,
    priority: Optional[int] = None,
    due_date: Optional[date] = None
) -> Todo:
    """
    Create a new todo item.
    
    Args:
        db: Database session (provided by FastAPI dependency injection)
        title: The text content of the todo
        
    Returns:
        The created Todo object
        
    Example:
        todo = await create_todo(db, "Buy milk")
    """
    # Create a new Todo object with the provided title
    # completed defaults to False (see the model definition)
    if priority is None:
        priority = calculate_priority_from_due_date(due_date)

    new_todo = Todo(
        title=title,
        completed=False,
        priority=priority,
        due_date=due_date
    )
    
    # Add the todo to the database session
    # Think of this as "staging" the change
    db.add(new_todo)
    
    # Commit the transaction - actually save it to the database
    # This is when it becomes permanent
    await db.commit()
    
    # Refresh the object to get the auto-generated ID from the database
    await db.refresh(new_todo)
    
    return new_todo


async def get_all_todos(
    db: AsyncSession,
    completed: Optional[bool] = None,
    priority: Optional[int] = None
) -> List[Todo]:
    """
    Retrieve all todos from the database.
    
    Args:
        db: Database session
        
    Returns:
        List of all Todo objects
        
    Example:
        todos = await get_all_todos(db)
        for todo in todos:
            print(todo.title)
    """
    # Create a SQL SELECT query using SQLModel
    # select(Todo) is equivalent to "SELECT * FROM todo"
    statement = select(Todo)

    if completed is not None:
        statement = statement.where(Todo.completed == completed)
    if priority is not None:
        statement = statement.where(Todo.priority == priority)

    # Show higher-priority tasks first, then by newest id
    statement = statement.order_by(Todo.priority.desc(), Todo.id.desc())
    
    # Execute the query and get the results
    result = await db.execute(statement)
    
    # Extract all todos from the result
    # scalars().all() converts the result rows into Todo objects
    todos = result.scalars().all()
    
    return todos


async def get_todo_by_id(db: AsyncSession, todo_id: int) -> Optional[Todo]:
    """
    Retrieve a specific todo by its ID.
    
    Args:
        db: Database session
        todo_id: The unique identifier of the todo
        
    Returns:
        Todo object if found, None if not found
        
    Example:
        todo = await get_todo_by_id(db, 1)
        if todo:
            print(todo.title)
    """
    # Create a SELECT query with a WHERE clause
    # This is equivalent to "SELECT * FROM todo WHERE id = todo_id"
    statement = select(Todo).where(Todo.id == todo_id)
    
    # Execute the query
    result = await db.execute(statement)
    
    # Get the first result, or None if not found
    # scalar_one_or_none() returns the object or None (not a list)
    todo = result.scalar_one_or_none()
    
    return todo


async def update_todo(
    db: AsyncSession,
    todo_id: int,
    title: Optional[str] = None,
    completed: Optional[bool] = None,
    priority: Optional[int] = None,
    due_date: Optional[date] = None,
    priority_provided: bool = False,
    due_date_provided: bool = False
) -> Todo:
    """
    Update an existing todo item.
    
    Args:
        db: Database session
        todo_id: The unique identifier of the todo to update
        title: New title (optional - only updates if provided)
        completed: New completion status (optional - only updates if provided)
        
    Returns:
        The updated Todo object
        
    Raises:
        HTTPException: If the todo doesn't exist
        
    Example:
        todo = await update_todo(db, 1, title="Buy eggs", completed=True)
    """
    # First, get the todo from the database
    todo = await get_todo_by_id(db, todo_id)
    
    # Check if the todo exists
    if not todo:
        # Raise an HTTP 404 error if not found
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    
    # Update only the fields that were provided (not None)
    # This allows partial updates
    if title is not None:
        todo.title = title
    if completed is not None:
        todo.completed = completed
    if priority_provided and priority is not None:
        todo.priority = priority
    if due_date_provided:
        todo.due_date = due_date
        if not priority_provided:
            todo.priority = calculate_priority_from_due_date(todo.due_date)
    
    # Add the updated todo to the session (SQLAlchemy tracks changes automatically)
    db.add(todo)
    
    # Commit the changes to the database
    await db.commit()
    
    # Refresh to get the latest data
    await db.refresh(todo)
    
    return todo


async def delete_todo(db: AsyncSession, todo_id: int) -> bool:
    """
    Delete a todo item from the database.
    
    Args:
        db: Database session
        todo_id: The unique identifier of the todo to delete
        
    Returns:
        True if deleted successfully, False if not found
        
    Raises:
        HTTPException: If the todo doesn't exist
        
    Example:
        success = await delete_todo(db, 1)
    """
    # Get the todo first
    todo = await get_todo_by_id(db, todo_id)
    
    # Check if it exists
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    
    # Delete the todo from the database session
    await db.delete(todo)
    
    # Commit the deletion
    await db.commit()
    
    return True
