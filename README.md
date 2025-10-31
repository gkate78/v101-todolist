# Todo List App - MVC Architecture Tutorial

A simple todo list application built with FastAPI following the MVC (Model-View-Controller) architecture pattern. This project is designed to teach the basics of web application development.

## 🎯 Learning Objectives

This project demonstrates:

1. **SQL/Database Layer** - How to define database tables and interact with them
2. **Controller Layer** - Business logic and data operations
3. **View Layer** - User interface with templates
4. **MVC Architecture** - How to organize code into Models, Views, and Controllers

## 📁 Project Structure

```
v101-todolist/
├── app/
│   ├── __init__.py
│   ├── database.py          # Database configuration and connection
│   ├── models/              # Database models (SQL layer)
│   │   ├── __init__.py
│   │   └── todo.py          # Todo table definition
│   ├── controllers/         # Business logic layer
│   │   ├── __init__.py
│   │   └── todo_controller.py  # CRUD operations
│   ├── routes/              # API endpoints and HTTP handling
│   │   ├── __init__.py
│   │   └── todo_routes.py   # REST API routes
│   ├── templates/           # HTML templates (View layer)
│   │   ├── base.html        # Base template with navigation
│   │   └── index.html       # Todo list page
│   └── utils/               # Utility functions
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd v101-todolist
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

5. **Access the application:**
   - Web Interface: http://localhost:8000/api/todos/
   - API Documentation (Swagger): http://localhost:8000/docs
   - Alternative API Docs: http://localhost:8000/redoc

## 📚 Learning Path

### 1. SQL/Database Layer (Start Here!)

**Files to study:**
- `app/database.py` - Database setup and connection
- `app/models/todo.py` - Todo table structure

**Key concepts:**
- SQLModel: Defining database tables using Python classes
- AsyncSession: Asynchronous database operations
- Primary keys and field types

### 2. Controller Layer (Business Logic)

**Files to study:**
- `app/controllers/todo_controller.py` - CRUD operations

**Key concepts:**
- Create: Adding new todos
- Read: Retrieving todos (all or by ID)
- Update: Modifying existing todos
- Delete: Removing todos

### 3. API Routes (HTTP Endpoints)

**Files to study:**
- `app/routes/todo_routes.py` - REST API endpoints

**Key concepts:**
- HTTP methods (GET, POST, PUT, DELETE)
- Pydantic schemas for data validation
- Swagger/OpenAPI documentation
- Request/Response handling

**Test the API using Swagger:**
1. Go to http://localhost:8000/docs
2. Try the endpoints interactively
3. See request/response examples

### 4. View Layer (Templates)

**Files to study:**
- `app/templates/base.html` - Base template
- `app/templates/index.html` - Todo list page

**Key concepts:**
- Jinja2 templating
- TailwindCSS styling
- JavaScript for interactivity
- Form handling

## 🔧 API Endpoints

### Create Todo
- **Method:** POST
- **URL:** `/api/todos/`
- **Body:** `{"title": "Your todo text"}`

### Get All Todos
- **Method:** GET
- **URL:** `/api/todos/list`

### Get Todo by ID
- **Method:** GET
- **URL:** `/api/todos/{todo_id}`

### Update Todo
- **Method:** PUT
- **URL:** `/api/todos/{todo_id}`
- **Body:** `{"title": "New title", "completed": true}`

### Delete Todo
- **Method:** DELETE
- **URL:** `/api/todos/{todo_id}`

## 🎓 Teaching Notes

### MVC Architecture Explained

1. **Model (app/models/)**
   - Defines the database structure
   - Represents data entities (Todo)
   - Maps Python objects to database tables

2. **View (app/templates/)**
   - User interface (HTML templates)
   - Presents data to users
   - Handles user interactions

3. **Controller (app/controllers/)**
   - Contains business logic
   - Processes requests
   - Interacts with models
   - Returns data to views

4. **Routes (app/routes/)**
   - Maps URLs to controller functions
   - Handles HTTP requests/responses
   - Validates input data

### Code Organization Benefits

- **Separation of Concerns:** Each layer has a specific responsibility
- **Testability:** Easy to test each component independently
- **Maintainability:** Changes in one layer don't affect others
- **Scalability:** Easy to add new features

## 📝 Notes for Students

1. **Read the comments!** Every file has detailed comments explaining what's happening.

2. **Start with the database:** Understanding the data structure helps understand everything else.

3. **Use Swagger:** The interactive docs at `/docs` are your best friend for testing the API.

4. **Experiment:** Try modifying the code to see what happens!

5. **Follow the flow:** Request → Route → Controller → Model → Database → Response

## 🐛 Troubleshooting

**Database errors?**
- Delete `database.db` and restart the app (it will recreate)

**Port already in use?**
- Change the port in `main.py` (line with `port=8000`)

**Import errors?**
- Make sure you're in the project directory
- Make sure your virtual environment is activated

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)

## 🎨 Design

This app follows the Vibecamp design system:
- Clean black and white aesthetic
- Kalam font for headings (handwritten style)
- Inter font for body text
- Mobile-first responsive design

---

**Happy Learning!** 🚀
