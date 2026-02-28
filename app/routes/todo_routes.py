"""
Todo Routes - API Endpoint Definitions

This module defines the HTTP API endpoints for todo operations.
Routes handle:
- Receiving HTTP requests (GET, POST, PUT, DELETE)
- Validating input data
- Calling controller functions
- Returning HTTP responses

OpenAPI/Swagger Documentation:
FastAPI automatically generates interactive API documentation.
You can access it at: http://localhost:8000/docs

Pydantic Schemas:
- TodoCreate: Used to validate data when creating a todo
- TodoUpdate: Used to validate data when updating a todo
- TodoResponse: Defines the structure of the response
"""

from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.database import get_db
from app.controllers.todo_controller import (
    create_todo,
    get_all_todos,
    get_todo_by_id,
    update_todo,
    delete_todo
)

# Create a router for todo-related endpoints
# prefix="/api/todos" means all routes will start with /api/todos
# tags=["todos"] groups these endpoints in Swagger documentation
router = APIRouter(prefix="/api/todos", tags=["todos"])

# Initialize Jinja2 templates for HTML responses
templates = Jinja2Templates(directory="app/templates")


# ============================================================================
# Pydantic Schemas - Data Validation and Serialization
# ============================================================================

class TodoCreate(BaseModel):
    """
    Schema for creating a new todo.
    
    This defines what data is required/expected when creating a todo.
    FastAPI automatically validates incoming JSON against this schema.
    """
    title: str  # Required field - must be a string
    priority: int | None = Field(default=None, ge=1, le=3)
    due_date: date | None = None


class TodoUpdate(BaseModel):
    """
    Schema for updating an existing todo.
    
    All fields are Optional, so you can update just the title,
    just the completed status, or both.
    """
    title: str | None = None  # Optional - can be None
    completed: bool | None = None  # Optional - can be None
    priority: int | None = Field(default=None, ge=1, le=3)
    due_date: date | None = None


class TodoResponse(BaseModel):
    """
    Schema for todo responses.
    
    This defines the structure of data returned by the API.
    It ensures consistent response formatting.
    """
    id: int
    title: str
    completed: bool
    priority: int
    due_date: date | None
    
    # Tell Pydantic to read from SQLModel objects
    model_config = {
        "from_attributes": True  # Allows conversion from SQLModel objects
    }


# ============================================================================
# API Endpoints (REST API)
# ============================================================================

@router.post("/", response_model=TodoResponse, status_code=201)
async def create_todo_endpoint(
    todo_data: TodoCreate,
    db: AsyncSession = Depends(get_db)
) -> TodoResponse:
    """
    Create a new todo item.
    
    **Swagger Documentation:**
    - Method: POST
    - URL: /api/todos/
    - Request Body: JSON with "title" field
    - Response: Created todo object (status 201)
    
    **Example Request:**
    ```json
    {
        "title": "Buy groceries"
    }
    ```
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "title": "Buy groceries",
        "completed": false
    }
    ```
    """
    # Call the controller function to handle the business logic
    todo = await create_todo(
        db,
        todo_data.title,
        priority=todo_data.priority,
        due_date=todo_data.due_date
    )
    
    # Convert SQLModel object to Pydantic response model
    return TodoResponse.model_validate(todo)


@router.get("/list", response_model=List[TodoResponse])
async def get_all_todos_endpoint(
    completed: bool | None = Query(default=None),
    priority: int | None = Query(default=None, ge=1, le=3),
    db: AsyncSession = Depends(get_db)
) -> List[TodoResponse]:
    """
    Get all todos (API endpoint).
    
    **Swagger Documentation:**
    - Method: GET
    - URL: /api/todos/list
    - Response: List of all todos (status 200)
    
    **Example Response:**
    ```json
    [
        {
            "id": 1,
            "title": "Buy groceries",
            "completed": false
        },
        {
            "id": 2,
            "title": "Finish homework",
            "completed": true
        }
    ]
    ```
    """
    # Get all todos from the controller
    todos = await get_all_todos(db, completed=completed, priority=priority)
    
    # Convert each SQLModel object to Pydantic response model
    return [TodoResponse.model_validate(todo) for todo in todos]


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo_endpoint(
    todo_id: int,
    db: AsyncSession = Depends(get_db)
) -> TodoResponse:
    """
    Get a specific todo by ID.
    
    **Swagger Documentation:**
    - Method: GET
    - URL: /api/todos/{todo_id}
    - Path Parameter: todo_id (integer)
    - Response: Todo object or 404 if not found
    
    **Example Request:**
    - URL: /api/todos/1
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "title": "Buy groceries",
        "completed": false
    }
    ```
    """
    # Get the todo by ID
    todo = await get_todo_by_id(db, todo_id)
    
    # Check if it exists
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    
    # Return the todo
    return TodoResponse.model_validate(todo)


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo_endpoint(
    todo_id: int,
    todo_data: TodoUpdate,
    db: AsyncSession = Depends(get_db)
) -> TodoResponse:
    """
    Update an existing todo.
    
    **Swagger Documentation:**
    - Method: PUT
    - URL: /api/todos/{todo_id}
    - Path Parameter: todo_id (integer)
    - Request Body: JSON with "title" and/or "completed" fields
    - Response: Updated todo object
    
    **Example Request:**
    ```json
    {
        "title": "Buy organic groceries",
        "completed": true
    }
    ```
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "title": "Buy organic groceries",
        "completed": true
    }
    ```
    """
    # Update the todo using the controller
    update_data = todo_data.model_dump(exclude_unset=True)

    todo = await update_todo(
        db,
        todo_id,
        title=update_data.get("title"),
        completed=update_data.get("completed"),
        priority=update_data.get("priority"),
        due_date=update_data.get("due_date"),
        priority_provided="priority" in update_data,
        due_date_provided="due_date" in update_data
    )
    
    # Return the updated todo
    return TodoResponse.model_validate(todo)


@router.delete("/{todo_id}", status_code=204)
async def delete_todo_endpoint(
    todo_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a todo.
    
    **Swagger Documentation:**
    - Method: DELETE
    - URL: /api/todos/{todo_id}
    - Path Parameter: todo_id (integer)
    - Response: No content (status 204)
    
    **Example Request:**
    - URL: /api/todos/1
    
    **Example Response:**
    - Status: 204 No Content (empty body)
    """
    # Delete the todo
    await delete_todo(db, todo_id)
    
    # 204 No Content means successful deletion with no response body
    return None


# ============================================================================
# Web Page Routes (HTML Views)
# ============================================================================

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def todos_page(
    request: Request,
    status: str = Query(default="all", pattern="^(all|pending|completed)$"),
    priority: str = Query(default="all", pattern="^(all|1|2|3)$"),
    db: AsyncSession = Depends(get_db)
):
    """
    Render the main todos page (HTML view).
    
    This is the web interface where users can see and manage todos.
    include_in_schema=False means this won't show up in Swagger docs
    (since it returns HTML, not JSON).
    
    **URL:** /api/todos/
    **Method:** GET
    **Response:** HTML page
    """
    # Get all todos from the database
    completed_filter = None
    if status == "pending":
        completed_filter = False
    elif status == "completed":
        completed_filter = True

    priority_filter = int(priority) if priority != "all" else None
    todos = await get_all_todos(db, completed=completed_filter, priority=priority_filter)
    
    # Render the HTML template with the todos data
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,  # Required by Jinja2
            "todos": todos,  # Pass todos to the template
            "selected_status": status,
            "selected_priority": priority
        }
    )
