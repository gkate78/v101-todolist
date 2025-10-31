"""
FastAPI Application Entry Point

This is the main file that starts the FastAPI web application.
It sets up:
- The FastAPI app instance
- Database initialization
- Route registration
- Static file serving
- Template rendering

When you run this file, it starts a web server that you can access at:
http://localhost:8000

You can also access:
- API Documentation (Swagger): http://localhost:8000/docs
- Alternative API Docs: http://localhost:8000/redoc
- Web Interface: http://localhost:8000/
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Import database initialization function
from app.database import init_db

# Import routes
from app.routes.todo_routes import router as todos_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI.
    
    This function runs when the app starts up and shuts down.
    - On startup: Initialize the database (create tables)
    - On shutdown: Clean up resources (if needed)
    
    The 'yield' keyword separates startup from shutdown code.
    """
    # Startup: Initialize the database
    print("Initializing database...")
    await init_db()
    print("Database initialized!")
    
    yield  # The app runs here
    
    # Shutdown: Add any cleanup code here if needed
    print("Shutting down...")


# Create the FastAPI application instance
app = FastAPI(
    title="Todo List API",  # Appears in Swagger documentation
    description="A simple todo list application demonstrating MVC architecture",  # Description in docs
    version="1.0.0",  # API version
    lifespan=lifespan  # Use our lifespan manager
)

# Mount static files (CSS, JS, images)
# Files in app/static/ will be accessible at /static/
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
# This connects our route definitions to the FastAPI app
app.include_router(todos_router)


# Root route - redirects to the todos page
@app.get("/")
async def root():
    """
    Root endpoint - redirects to the todos page.
    
    This is the first thing users see when they visit the app.
    """
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/api/todos/")


# Run the application
# This code only runs if you execute this file directly
if __name__ == "__main__":
    import uvicorn
    
    # Start the server
    # host="0.0.0.0" means listen on all network interfaces
    # port=8000 is the port number
    # reload=True enables auto-reload on code changes (great for development!)
    uvicorn.run(
        "main:app",  # Reference to our FastAPI app
        host="0.0.0.0",
        port=8000,
        reload=True
    )

