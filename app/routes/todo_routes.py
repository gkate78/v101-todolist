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

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

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


class TodoUpdate(BaseModel):
    """
    Schema for updating an existing todo.
    
    All fields are Optional, so you can update just the title,
    just the completed status, or both.
    """
    title: str | None = None  # Optional - can be None
    completed: bool | None = None  # Optional - can be None


class TodoResponse(BaseModel):
    """
    Schema for todo responses.
    
    This defines the structure of data returned by the API.
    It ensures consistent response formatting.
    """
    id: int
    title: str
    completed: bool
    
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
    todo = await create_todo(db, todo_data.title)
    
    # Convert SQLModel object to Pydantic response model
    return TodoResponse.model_validate(todo)


@router.get("/list", response_model=List[TodoResponse])
async def get_all_todos_endpoint(
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
    todos = await get_all_todos(db)
    
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
    todo = await update_todo(
        db,
        todo_id,
        title=todo_data.title,
        completed=todo_data.completed
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
async def todos_page(request: Request, db: AsyncSession = Depends(get_db)):
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
    todos = await get_all_todos(db)
    
    # Render the HTML template with the todos data
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,  # Required by Jinja2
            "todos": todos  # Pass todos to the template
        }
    )

