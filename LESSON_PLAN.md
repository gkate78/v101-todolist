# Todo List App - Lesson Plan
## MVC Architecture Teaching Guide

**Total Duration:** 4 hours 2 minutes (4 sessions of 1 hour each + 2-minute intro)  
**Target Audience:** Students learning web development basics  
**Prerequisites:** Basic Python knowledge, understanding of web concepts (HTML, HTTP)

---

## Pre-Lesson: Introduction to Cursor & Development Environment (2 minutes)
### Setting Up for Success

### Learning Objectives
By the end of this brief introduction, students will understand:
- What Cursor is and why we use it
- What Cursor rules (.mdc files) are and their purpose
- How project rules guide code structure and best practices

### Topics to Cover

#### Part 1: What is Cursor? (1 minute)
**Key Points:**
- Cursor is a code editor built for AI-assisted development
- It helps with code suggestions, explanations, and following best practices
- Think of it as a smart coding assistant that understands your project

**Teaching Points:**
- Cursor = VS Code + AI capabilities
- It helps maintain consistent code style across the project
- It can explain code, suggest improvements, and catch errors

#### Part 2: Understanding Cursor Rules (.mdc files) (1 minute)
**Key Points:**
- `.mdc` files are "Cursor rules" - guidelines for the AI assistant
- They define project structure, coding standards, and best practices
- The AI uses these rules to help write code that matches the project style

**Teaching Points:**
- `.mdc` = Markdown Cursor rules file
- Located in `.cursor/rules/` directory
- Contains: architecture guidelines, coding standards, design patterns
- Example: Our project has `fastapi-mvc.mdc` that enforces MVC structure

**Visual Example:**
```
.cursor/
  └── rules/
      └── fastapi-mvc.mdc    →  Contains our project rules
```

**Why It Matters:**
- Ensures all code follows the same patterns
- Makes the project easier to understand and maintain
- Helps AI assistant provide better suggestions
- Think of it as a "style guide" for the entire project

**Takeaway:**
- Students don't need to memorize the rules
- Just understand that Cursor uses these rules to help maintain code quality
- The rules ensure our MVC architecture is followed consistently

**Note to Instructor:**
- Briefly show the `.cursor/rules/fastapi-mvc.mdc` file if appropriate
- Explain that these rules help maintain the MVC structure we'll be learning
- This sets context for why code is organized the way it is

---

## Session 1: Databases & SQL (1 Hour)
### Understanding the Data Layer

### Learning Objectives
By the end of this session, students will be able to:
- Understand what a database is and why we need it
- Explain the relationship between Python objects and database tables
- Read and understand SQLModel model definitions
- Identify primary keys, field types, and constraints
- Understand database sessions and connections

### Time Breakdown

#### Part 1: Introduction (10 minutes)
**Topics to Cover:**
- What is a database? Why do we need one?
- SQLite vs other databases (brief comparison)
- Data persistence: storing data beyond a single request
- Introduction to ORM (Object-Relational Mapping)

**Teaching Points:**
- Use analogies: Database = filing cabinet, Table = folder, Row = document
- Show the `database.db` file (if it exists) to make it tangible
- Explain that SQLite stores data in a file (good for learning)

#### Part 2: Exploring the Database Configuration (15 minutes)
**File to Focus On:** `app/database.py`

**Key Concepts to Explain:**
```python
# Show these concepts:
1. DATABASE_URL - connection string
2. create_async_engine() - creates the database connection pool
3. AsyncSessionLocal - session factory
4. get_db() - dependency injection function
5. init_db() - creates tables on startup
```

**Teaching Strategy:**
- Walk through `database.py` line by line
- Explain what each function does
- Show how FastAPI uses `Depends(get_db)` to provide database access
- Demonstrate the `echo=True` option (show SQL queries in console)

**Interactive Exercise:**
- Have students modify `DATABASE_URL` to see how it changes
- Show them how `echo=True` prints SQL to console
- Explain async vs sync database operations briefly

#### Part 3: Understanding the Todo Model (20 minutes)
**File to Focus On:** `app/models/todo.py`

**Key Concepts:**
```python
# Break down the Todo class:
1. Class Todo extends SQLModel
2. table=True - makes it a database table
3. id: Optional[int] - primary key, auto-generated
4. title: str - required field with max length
5. completed: bool - boolean field with default value
```

**Teaching Points:**
- Explain that a Python class becomes a database table
- Show how Field() adds constraints (max_length, default)
- Explain primary keys (unique identifier for each row)
- Discuss data types: str, int, bool and their SQL equivalents
- Optional vs required fields

**Visual Aid:**
```
Python Class          →  Database Table
─────────────────           ─────────────
Todo                   →    todo
  id: int              →    id (INTEGER PRIMARY KEY)
  title: str           →    title (TEXT NOT NULL)
  completed: bool      →    completed (BOOLEAN DEFAULT 0)
```

**Hands-On Activity:**
- Ask students to add a new field to the Todo model (e.g., `priority: int = Field(default=1)`)
- Show how the database creates a new column
- Explain migrations briefly (optional, advanced)

#### Part 4: Database Operations Overview (10 minutes)
**File to Reference:** `app/controllers/todo_controller.py` (just the concepts, not implementation)

**Concepts to Introduce:**
- CRUD operations: Create, Read, Update, Delete
- Database sessions: think of it as a conversation with the database
- Transactions: commit (save) vs rollback (cancel)
- Why we use async/await for database operations

**Mental Model:**
```
1. Open session (start conversation)
2. Make changes (add, modify, query)
3. Commit changes (save to database)
4. Close session (end conversation)
```

#### Part 5: Q&A and Wrap-up (5 minutes)
- Review key concepts
- Answer questions
- Preview: "Next time we'll see how to use this database through an API"

### Session 1 Assessment Questions
1. What is the purpose of a primary key?
2. What does `table=True` do in SQLModel?
3. Why do we use `Optional[int]` for the id field?
4. What happens when you call `init_db()`?

### Session 1 Homework/Practice
- Have students add a new field to the Todo model (e.g., `description: str | None = None`)
- Ask them to explain in their own words what each part of the model does
- Optional: Show them how to query the database directly using a SQLite browser

---

## Session 2: APIs & Swagger Documentation (1 Hour)
### Understanding the Controller and Route Layers

### Learning Objectives
By the end of this session, students will be able to:
- Understand what an API is and how it works
- Identify REST API endpoints (GET, POST, PUT, DELETE)
- Use Swagger UI to interact with APIs
- Understand Pydantic schemas for validation
- Trace a request from HTTP to database and back

### Time Breakdown

#### Part 1: Introduction to APIs (10 minutes)
**Topics to Cover:**
- What is an API? (Application Programming Interface)
- REST API basics: URLs as resources, HTTP methods as actions
- Request/Response cycle
- JSON format (JavaScript Object Notation)

**Teaching Points:**
- Use analogies: API = restaurant menu, you order (request), kitchen prepares (processing), you get food (response)
- Show HTTP methods as verbs:
  - GET = "read" or "fetch"
  - POST = "create" or "send new"
  - PUT = "update" or "replace"
  - DELETE = "remove"

**Visual Example:**
```
Client (Browser)  →  HTTP Request  →  FastAPI Server  →  Database
                                                        ↓
Client (Browser)  ←  HTTP Response ←  FastAPI Server  ←  Database
```

#### Part 2: Exploring the Controller Layer (15 minutes)
**File to Focus On:** `app/controllers/todo_controller.py`

**Key Concepts:**
```python
# Show the CRUD functions:
1. create_todo() - adds new todo
2. get_all_todos() - retrieves all todos
3. get_todo_by_id() - gets one specific todo
4. update_todo() - modifies existing todo
5. delete_todo() - removes a todo
```

**Teaching Strategy:**
- Walk through one function in detail (e.g., `create_todo`)
- Show the flow: receive data → validate → database operation → return result
- Explain error handling (HTTPException)
- Show how database session is used

**Code Walkthrough Example (create_todo):**
```python
# Step 1: Create Python object
new_todo = Todo(title=title, completed=False)

# Step 2: Add to database session (staging)
db.add(new_todo)

# Step 3: Commit to database (save permanently)
await db.commit()

# Step 4: Refresh to get auto-generated ID
await db.refresh(new_todo)
```

**Concept to Emphasize:**
- Controllers contain business logic
- They don't know about HTTP - they just work with data
- Separation of concerns: controllers handle logic, routes handle HTTP

#### Part 3: Understanding Routes & Endpoints (20 minutes)
**File to Focus On:** `app/routes/todo_routes.py`

**Key Concepts to Cover:**

**1. Pydantic Schemas (10 minutes)**
```python
# Explain these schemas:
TodoCreate  →  Validates incoming data for creating
TodoUpdate  →  Validates incoming data for updating
TodoResponse →  Defines output format
```

**Teaching Points:**
- Why validation? Prevents bad data, clear error messages
- Show how FastAPI automatically validates based on schema
- Demonstrate what happens with invalid data

**2. API Endpoints (10 minutes)**
Show each endpoint and explain:

```python
POST   /api/todos/         →  Create new todo
GET    /api/todos/list     →  Get all todos
GET    /api/todos/{id}     →  Get one todo
PUT    /api/todos/{id}     →  Update a todo
DELETE /api/todos/{id}     →  Delete a todo
```

**URL Structure Explanation:**
- `/api/todos/` - collection of todos
- `/api/todos/1` - specific todo with ID 1
- HTTP method determines the action

**Request/Response Examples:**
Show students what requests and responses look like:
- Request body (JSON)
- Response status codes (200, 201, 404, etc.)
- Response body (JSON)

#### Part 4: Hands-On with Swagger UI (20 minutes)
**URL:** http://localhost:8000/docs

**Teaching Strategy:**
1. **Introduce Swagger (5 minutes)**
   - What is it? Interactive API documentation
   - Why is it useful? Test APIs without writing code
   - Show the interface

2. **Walk Through Each Endpoint (15 minutes)**
   - Start with GET (easiest to understand)
   - Show how to expand an endpoint
   - Explain: "Try it out" button
   - Show request/response examples
   - Demonstrate POST with JSON body
   - Show validation errors (try invalid data)

**Interactive Demo Flow:**
```
1. GET /api/todos/list
   - Show empty list or existing todos
   - Explain JSON response format

2. POST /api/todos/
   - Click "Try it out"
   - Enter JSON: {"title": "Learn APIs"}
   - Execute → See response
   - Show 201 status code

3. GET /api/todos/{id}
   - Use the ID from step 2
   - Show how to get one specific todo

4. PUT /api/todos/{id}
   - Update the todo: {"title": "Master APIs", "completed": true}
   - Show updated response

5. DELETE /api/todos/{id}
   - Delete the todo
   - Show 204 No Content response
```

**Key Teaching Moments:**
- Status codes: 200 (success), 201 (created), 204 (no content), 404 (not found)
- Request vs Response: What you send vs what you get back
- JSON format: Key-value pairs, arrays, nested objects

#### Part 5: Request Flow Demonstration (10 minutes)
**Show the Complete Flow:**

```
Browser → Route → Controller → Database → Controller → Route → Browser
```

**Step-by-Step Example (Creating a Todo):**

1. **Request arrives:** POST /api/todos/ with JSON body
2. **Route receives it:** `create_todo_endpoint()` function
3. **Validation:** FastAPI validates JSON against `TodoCreate` schema
4. **Route calls controller:** `await create_todo(db, todo_data.title)`
5. **Controller does work:** Creates Todo object, saves to database
6. **Controller returns:** Todo object
7. **Route formats response:** Converts to `TodoResponse` schema
8. **Response sent:** JSON back to client

**Visual Flow Diagram:**
```
POST /api/todos/
  ↓
todo_routes.py: create_todo_endpoint()
  ↓
Validates with TodoCreate schema
  ↓
todo_controller.py: create_todo()
  ↓
database.py: Uses db session
  ↓
Creates Todo in database.db
  ↓
Returns TodoResponse JSON
```

#### Part 6: Q&A and Wrap-up (5 minutes)
- Review key concepts: REST API, HTTP methods, endpoints
- Remind students: Controllers = logic, Routes = HTTP handling
- Preview: "Next time we'll build the user interface that uses these APIs"

### Session 2 Assessment Questions
1. What HTTP method would you use to update a todo?
2. What is the purpose of Pydantic schemas?
3. What does a 404 status code mean?
4. What's the difference between a route and a controller?

### Session 2 Homework/Practice
- Use Swagger to create 3 todos
- Practice updating and deleting todos via Swagger
- Write down what JSON you would send to create a todo with title "Buy groceries"
- Try to call an API endpoint that doesn't exist and see what happens

---

## Session 3: Frontend Templates & User Interface (1 Hour)
### Understanding the View Layer

### Learning Objectives
By the end of this session, students will be able to:
- Understand how templates work (Jinja2)
- Explain how frontend JavaScript interacts with backend APIs
- Identify the flow from user action to database update
- Understand the separation between presentation and logic
- Recognize HTML, CSS (Tailwind), and JavaScript working together

### Time Breakdown

#### Part 1: Introduction to Templates (10 minutes)
**Topics to Cover:**
- What are templates? Reusable HTML with dynamic content
- Server-side rendering vs client-side rendering (brief)
- Jinja2 template engine basics
- Template inheritance (base.html → index.html)

**Teaching Points:**
- Templates = HTML with placeholders that get filled with data
- Server renders template → sends complete HTML to browser
- Show the difference between static HTML and dynamic templates

**Visual Example:**
```
Template (with variables):
  <h1>{{ todo.title }}</h1>
  
After rendering (with data):
  <h1>Buy groceries</h1>
```

#### Part 2: Exploring the Base Template (10 minutes)
**File to Focus On:** `app/templates/base.html`

**Key Concepts:**
```html
<!-- Show these Jinja2 features: -->
{% block title %} ... {% endblock %}    →  Defines replaceable sections
{% extends "base.html" %}                →  Template inheritance
{% block content %} ... {% endblock %}  →  Where child templates put content
```

**Teaching Strategy:**
- Explain template inheritance: base.html = layout, other templates = pages
- Show the structure: head, navigation, content area, footer
- Explain TailwindCSS: utility classes for styling (brief overview)
- Point out: This template provides the page structure, other templates fill in content

**Key Points:**
- Base template = reusable layout (like a frame)
- Child templates extend base and fill in blocks
- Separation: Layout (base) vs Content (index.html)

#### Part 3: Understanding the Todo List Template (20 minutes)
**File to Focus On:** `app/templates/index.html`

**Part 3A: Template Syntax (10 minutes)**

**Jinja2 Features to Cover:**
```jinja
{% extends "base.html" %}           →  Inherits from base
{% block content %} ... {% endblock %} →  Defines content section
{% for todo in todos %} ... {% endfor %} →  Loops through todos
{% if todo.completed %} ... {% endif %} →  Conditional rendering
{{ todo.title }}                    →  Outputs variable value
```

**Teaching Strategy:**
- Show how the template loops through todos from the database
- Explain conditional rendering (show different states for completed/pending)
- Show how data flows: Route → Template → HTML

**Code Walkthrough:**
```jinja
{# This loop runs for each todo in the list #}
{% for todo in todos %}
  <div>
    {# Show the todo title #}
    <h3>{{ todo.title }}</h3>
    
    {# Conditional: Show different text if completed #}
    {% if todo.completed %}
      <p>Completed</p>
    {% else %}
      <p>Pending</p>
    {% endif %}
  </div>
{% endfor %}
```

**Part 3B: HTML Structure (10 minutes)**
- Show the form structure (Add Todo form)
- Explain form submission (POST request)
- Show how todos are displayed (list structure)
- Point out semantic HTML: forms, buttons, lists

#### Part 4: JavaScript & API Integration (25 minutes)
**File to Focus On:** `app/templates/index.html` (JavaScript section)

**Part 4A: Understanding JavaScript Functions (10 minutes)**

**Key Functions to Explain:**

1. **Form Submission Handler**
```javascript
// When form is submitted, prevent default (no page reload)
// Get input value, send POST request to API
// Reload page to show new todo
```

2. **Toggle Todo Function**
```javascript
// Called when checkbox is clicked
// Sends PUT request to update completed status
```

3. **Delete Todo Function**
```javascript
// Asks for confirmation
// Sends DELETE request
```

4. **Edit Functions** (startEdit, saveEdit, cancelEdit)
```javascript
// Switches between display and edit mode
// Sends PUT request to update title
```

**Teaching Strategy:**
- Explain fetch API: How JavaScript makes HTTP requests
- Show the connection: JavaScript calls → API endpoints → Database
- Explain async/await: Waiting for server response
- Show error handling: try/catch blocks

**Part 4B: API Call Examples (10 minutes)**

**Walk Through One Function in Detail:**

```javascript
async function toggleTodo(todoId, completed) {
  // 1. Make HTTP request
  const response = await fetch(`${API_BASE_URL}/${todoId}`, {
    method: 'PUT',  // HTTP method
    headers: {
      'Content-Type': 'application/json',  // Tell server we're sending JSON
    },
    body: JSON.stringify({ completed: completed })  // Data to send
  });
  
  // 2. Check if request succeeded
  if (!response.ok) {
    throw new Error('Failed to update todo');
  }
  
  // 3. Update the page
  window.location.reload();
}
```

**Key Teaching Points:**
- `fetch()` = how JavaScript talks to the API
- `await` = wait for server response
- `JSON.stringify()` = convert JavaScript object to JSON string
- Error handling: what happens if something goes wrong

**Part 4C: User Interaction Flow (5 minutes)**

**Complete User Journey:**
```
1. User clicks checkbox
   ↓
2. JavaScript: toggleTodo(1, true)
   ↓
3. fetch() sends PUT /api/todos/1
   ↓
4. Route receives request
   ↓
5. Controller updates database
   ↓
6. Response sent back (success)
   ↓
7. JavaScript reloads page
   ↓
8. Page shows updated todo (with checkmark)
```

#### Part 5: Hands-On: Modifying the Template (15 minutes)
**Interactive Exercise:**

Have students make small modifications:

1. **Change the page title**
   - Find `{% block title %}` in index.html
   - Change "Todo List - Home" to something else
   - Refresh page to see change

2. **Add a new field display** (if time allows)
   - Show how to add more information to each todo card
   - Explain how data flows from database → template → screen

3. **Modify styling** (optional, brief)
   - Change a Tailwind class (e.g., `text-black` to `text-blue-600`)
   - Show how CSS classes work with Tailwind

**Key Teaching Moment:**
- Templates separate presentation from logic
- Changing template doesn't affect database or API
- Small changes = big visual impact

#### Part 6: Complete Flow Review (5 minutes)
**Show the Full Stack:**

```
User clicks "Add Todo" button
  ↓
JavaScript: Form submission handler
  ↓
POST /api/todos/ (fetch request)
  ↓
Route: create_todo_endpoint()
  ↓
Controller: create_todo()
  ↓
Database: Insert new row
  ↓
Response: Todo object (JSON)
  ↓
JavaScript: Reload page
  ↓
Route: todos_page() renders template
  ↓
Template: Loops through todos, shows new one
  ↓
User sees: New todo in list
```

**Emphasize:**
- Frontend (JavaScript) talks to backend (API)
- Backend talks to database
- Data flows: User → Frontend → API → Database → API → Frontend → User
- Each layer has a specific job (separation of concerns)

#### Part 7: Q&A and Wrap-up (5 minutes)
- Review: Templates, JavaScript, API integration
- Remind: MVC pattern - Model (database), View (templates), Controller (business logic)
- Full stack: Database ↔ API ↔ Frontend
- Answer questions
- Encourage experimentation

### Session 3 Assessment Questions
1. What does `{{ variable }}` do in Jinja2?
2. How does JavaScript communicate with the backend API?
3. What happens when you click the "Add Todo" button? (Trace the flow)
4. What's the difference between server-side rendering and client-side rendering?

### Session 3 Homework/Practice
- Modify the template to change the color scheme
- Add a new display field to show something different about todos
- Try to understand how the edit functionality works
- Experiment with adding console.log() to JavaScript functions to see data flow

---

## Additional Resources & Tips

### Teaching Tips
1. **Use Analogies:** Compare database to filing cabinet, API to restaurant menu, templates to form letters
2. **Show, Don't Just Tell:** Use Swagger UI for interactive learning
3. **Break Down Complex Concepts:** Start simple, add complexity gradually
4. **Encourage Questions:** Create a safe space for students to ask
5. **Relate to Real-World:** Show how these concepts apply to apps they use

### Common Student Questions & Answers

**Q: Why do we need a database?**
A: To persist data beyond a single request. Without it, data would disappear when the server restarts.

**Q: What's the difference between a route and a controller?**
A: Route handles HTTP (request/response), controller handles business logic (data operations).

**Q: Why use templates instead of just HTML?**
A: Templates allow dynamic content - same template shows different data for different users/requests.

**Q: Can I use this without JavaScript?**
A: Yes, but you'd lose interactivity. JavaScript makes the page responsive without full page reloads.

### Extension Activities (If Time Permits)

**Session 1 Extension:**
- Show students how to query database using SQL directly
- Introduce database relationships (one-to-many, etc.)

**Session 2 Extension:**
- Show how to test APIs with curl command
- Explain authentication (brief, high-level)
- Show API versioning concepts

**Session 3 Extension:**
- Introduce CSS concepts more deeply
- Show how to add new features (filtering, sorting)
- Introduce client-side frameworks (very brief, just awareness)

### Assessment Options

**Option 1: Practical Assessment**
- Have students add a new feature (e.g., priority field)
- Must modify: Model, Controller, Route, Template
- Tests understanding of all layers

**Option 2: Written Assessment**
- Explain MVC architecture in their own words
- Trace a user action through all layers
- Identify which file handles which responsibility

**Option 3: Presentation**
- Students present one part of the application
- Explain how their assigned layer works
- Demonstrate changes they made

### Troubleshooting Common Issues

**Database Errors:**
- Delete `database.db` and restart (recreates tables)
- Check that `init_db()` is called on startup

**API Not Working:**
- Check server is running
- Verify endpoint URL is correct
- Check browser console for JavaScript errors

**Template Not Rendering:**
- Check Jinja2 syntax ({% %}, {{ }})
- Verify template file is in correct directory
- Check that route is passing data to template

---

## Final Review & Next Steps

After completing all 3 sessions, students should understand:
- How data is stored (database/models)
- How data is accessed (API/routes/controllers)
- How data is displayed (templates/frontend)
- How all pieces work together (MVC pattern)

**Suggested Next Topics:**
- User authentication
- Database relationships
- More advanced JavaScript features
- Deployment basics
- Testing

---

## Session 4: Deployment to Fly.io (1 Hour)
### Making Your App Available on the Internet

### Learning Objectives
By the end of this session, students will be able to:
- Understand what deployment means and why we do it
- Explain the concept of containers and Docker
- Deploy a FastAPI application to Fly.io
- Configure persistent storage for databases using volumes
- Monitor and manage deployed applications
- Understand the difference between local development and production

### Time Breakdown

#### Part 1: Introduction to Deployment (10 minutes)
**Topics to Cover:**
- What is deployment? Making your app accessible on the internet
- Why deploy? Share your app, always available, professional
- Local vs Production: Development (your computer) vs Production (cloud servers)
- Introduction to containers: Package your app and its dependencies

**Teaching Points:**
- Use analogies: Deployment = publishing a book (local vs bookstore)
- Containers = shipping containers (consistent environment)
- Cloud platforms = rental servers (you don't own the hardware)

**Key Concepts:**
- **Local Development**: App runs on your computer (localhost:8000)
- **Production**: App runs on cloud servers (accessible via URL)
- **Container**: Package containing app + dependencies + runtime
- **Platform**: Service that runs containers (Fly.io, Heroku, etc.)

#### Part 2: Understanding Docker and Containers (15 minutes)
**File to Focus On:** `Dockerfile`

**Key Concepts:**
```dockerfile
# Explain each section:
1. FROM - Base image (Python environment)
2. WORKDIR - Working directory in container
3. ENV - Environment variables
4. RUN - Commands to run during build
5. COPY - Copy files into container
6. EXPOSE - Port the app listens on
7. CMD - Command to run when container starts
```

**Teaching Strategy:**
- Walk through Dockerfile line by line
- Explain that Dockerfile = recipe for building container
- Show how it packages Python + dependencies + code
- Demonstrate: One container = consistent environment everywhere

**Visual Example:**
```
Your Computer          →  Docker Container        →  Fly.io Server
─────────────────            ─────────────             ───────────
Code + Dependencies    →   Same Code + Deps     →   Same Container
Different setups       →   Consistent setup     →   Runs anywhere
```

**Hands-On Demo (if time permits):**
```bash
# Build container locally (optional demo)
docker build -t todo-app .
docker run -p 8000:8000 todo-app
```

#### Part 3: Fly.io Configuration (15 minutes)
**File to Focus On:** `fly.toml`

**Key Concepts to Explain:**
```toml
# Break down fly.toml:
1. app = "v101-todolist" - App name
2. primary_region - Where servers are located
3. http_service - HTTP configuration
4. [[mounts]] - Volume for database persistence
5. [[http_service.checks]] - Health checks
```

**Teaching Points:**
- `fly.toml` = instructions for Fly.io
- Region selection: Choose closest to users for speed
- Auto-start/stop: Saves money when app isn't used
- Health checks: Ensures app is running correctly

**Volume Mount Explanation:**
```toml
[[mounts]]
  source = "todo_db"        # Volume name
  destination = "/app/data" # Where it's mounted
```

**Why Volumes Matter:**
- Containers are temporary (can be destroyed/recreated)
- Volumes persist data across deployments
- Database needs permanent storage
- Without volume: data disappears when container restarts

#### Part 4: Database Persistence Setup (10 minutes)
**File to Focus On:** `app/database.py` (updated version)

**Key Concepts:**
```python
# Show how we configured for production:
DATABASE_DIR = os.getenv("DATABASE_DIR", "./")
DATABASE_FILE = os.path.join(DATABASE_DIR, "database.db")
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_FILE}"
```

**Teaching Points:**
- Environment variables: Different values for dev vs production
- Development: `./database.db` (local file)
- Production: `/app/data/database.db` (volume mount)
- Same code, different paths based on environment

**Visual Flow:**
```
Development:
  Code → ./database.db (local file)

Production:
  Code → /app/data/database.db (volume mount)
       → Fly.io Volume (persists forever)
```

#### Part 5: Deployment Walkthrough (15 minutes)
**Follow the DEPLOYMENT.md Guide Step-by-Step**

**Interactive Demo Flow:**

1. **Install Fly CLI (if not done)**
   ```bash
   # Show installation process
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login to Fly.io**
   ```bash
   fly auth login
   # Explain: Opens browser for authentication
   ```

3. **Create Volume for Database**
   ```bash
   fly volumes create todo_db --size 1 --region sin
   # Explain: Creates persistent storage
   # Show: Why we need this for database
   ```

4. **Set Environment Variable**
   ```bash
   fly secrets set DATABASE_DIR=/app/data
   # Explain: Tells app where to find database
   # Show: How this connects to code
   ```

5. **Connect GitHub Repository**
   - Go to Fly.io dashboard
   - Show: How to connect GitHub
   - Enable: Auto-deploy on push
   - Explain: Future deployments are automatic

6. **First Deployment**
   - Show: Fly.io building container
   - Explain: What happens during build
   - Watch: Logs to see startup
   - Verify: App is accessible via URL

**Key Teaching Moments:**
- Show the deployment process in real-time
- Explain each step as it happens
- Point out where to see errors (logs)
- Show how to verify it worked (fly status, fly logs)

#### Part 6: Post-Deployment Verification (5 minutes)

**Activities:**
1. **Check App Status**
   ```bash
   fly status
   # Show: App is running, healthy
   ```

2. **View Logs**
   ```bash
   fly logs
   # Show: Application output
   # Explain: Useful for debugging
   ```

3. **Test the App**
   - Open app URL in browser
   - Create a todo
   - Explain: Data is stored in volume
   - Show: App works just like local

4. **Verify Database Volume**
   ```bash
   fly ssh console -C "ls -la /app/data"
   # Show: database.db exists in volume
   ```

#### Part 7: Understanding the Deployment Flow (5 minutes)

**Complete Deployment Journey:**

```
1. Code in GitHub
   ↓
2. Fly.io detects push (or manual deploy)
   ↓
3. Builds Docker container
   ↓
4. Starts container on Fly.io server
   ↓
5. Mounts volume (database persistence)
   ↓
6. App runs and is accessible via URL
   ↓
7. Users can access your app on the internet!
```

**Key Concepts to Reinforce:**
- GitHub = Code storage
- Docker = Package your app
- Fly.io = Run your container
- Volume = Persistent storage
- URL = How users access your app

#### Part 8: Monitoring and Management (5 minutes)

**Common Tasks:**
```bash
# View logs (real-time)
fly logs

# Check status
fly status

# View metrics
fly metrics

# Open app in browser
fly open

# Restart app
fly apps restart

# Scale app (advanced)
fly scale count 2
```

**When Things Go Wrong:**
- Check logs first: `fly logs`
- Verify volume is mounted: `fly volumes list`
- Check environment variables: `fly secrets list`
- Restart if needed: `fly apps restart`

#### Part 9: Q&A and Wrap-up (5 minutes)
- Review key concepts: Docker, Fly.io, Volumes
- Answer questions
- Remind: Deployment makes your app accessible to the world
- Preview: Future topics (custom domains, scaling, monitoring)

### Session 4 Assessment Questions
1. What is the purpose of a Docker container?
2. Why do we need a volume for the database?
3. What's the difference between local development and production?
4. How does Fly.io know how to deploy your app?

### Session 4 Homework/Practice
- Deploy the app to Fly.io (if not done in class)
- Make a change to the app, push to GitHub, and watch it deploy
- Practice using Fly.io commands (status, logs, open)
- Write down the deployment steps in your own words
- Optional: Add a custom domain (if time permits)

### Troubleshooting Deployment Issues

**Build Fails:**
- Check Dockerfile syntax
- Verify all dependencies in requirements.txt
- Check logs: `fly logs`

**App Won't Start:**
- Check environment variables are set
- Verify database path is correct
- Check volume is mounted
- Review logs for errors

**Database Not Persisting:**
- Verify volume is created
- Check DATABASE_DIR is set correctly
- Verify volume mount in fly.toml
- Test with: `fly ssh console -C "ls -la /app/data"`

**Can't Access App:**
- Check app status: `fly status`
- Verify app is running: `fly logs`
- Check if URL is correct
- Verify HTTP service is configured

### Extension Activities

**Advanced Topics (If Time Permits):**
- Custom domain setup
- Setting up monitoring/alerting
- Backup strategies for databases
- CI/CD pipelines (GitHub Actions)
- Scaling applications

---

**Last Updated:** Generated for Todo List App Teaching  
**Version:** 2.0 (Added Deployment Session)

