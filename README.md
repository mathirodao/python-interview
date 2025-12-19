# python-interview / TodoAPI

[![Open in Coder](https://dev.crunchloop.io/open-in-coder.svg)](https://dev.crunchloop.io/templates/fly-containers/workspace?param.Git%20Repository=git@github.com:crunchloop/python-interview.git)

This is a simple Todo List API built with FastAPI and Python 3.13+. This project is currently being used for Python full-stack candidates.

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.13+** - Latest Python with full type hints
- **Pydantic v2** - Data validation using Python type annotations
- **In-memory storage** - Simple data persistence (resets on restart)
- **Poetry** - Modern dependency management
- **pytest** - Comprehensive unit tests with mocking
- **Ruff** - Extremely fast Python linter and formatter
- **mypy** - Static type checker with strict mode
- **DevContainer** - VS Code development container support

## Prerequisites

- Python 3.13+ or Docker with VS Code DevContainer support
- Poetry (if running locally without Docker)

## Installation

### Using Poetry (Local)

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Using DevContainer (Recommended)

1. Open the project in VS Code
2. Install the "Dev Containers" extension
3. Press `F1` and select "Dev Containers: Reopen in Container"
4. Dependencies will be installed automatically

## Running the app

### Development mode with hot reload

```bash
# Using Poetry
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or if inside poetry shell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production mode

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API docs (Swagger)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

All endpoints are prefixed with `/api/todolists`:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/todolists` | Get all todo lists |
| GET | `/api/todolists/{id}` | Get a specific todo list |
| POST | `/api/todolists` | Create a new todo list |
| PUT | `/api/todolists/{id}` | Update an existing todo list |
| DELETE | `/api/todolists/{id}` | Delete a todo list |

## Testing

```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=app --cov-report=html

# Run tests in watch mode
poetry run pytest-watch

# Run tests with verbose output
poetry run pytest -v
```

## Code Quality

### Linting and Formatting with Ruff

```bash
# Check for linting errors
poetry run ruff check .

# Fix linting errors automatically
poetry run ruff check --fix .

# Format code
poetry run ruff format .
```

### Type Checking with mypy

```bash
# Run type checker
poetry run mypy app/

# Run type checker on all files
poetry run mypy .
```

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # Pydantic models (schemas)
│   ├── routers/
│   │   ├── __init__.py
│   │   └── todo_lists.py    # TodoList API endpoints
│   └── services/
│       ├── __init__.py
│       └── todo_lists.py    # Business logic and in-memory storage
├── tests/
│   ├── __init__.py
│   └── test_todo_lists.py   # Unit tests for all endpoints
├── .devcontainer/           # VS Code DevContainer configuration
├── pyproject.toml           # Poetry dependencies and tool configs
├── .ruff.toml              # Ruff linter/formatter configuration
├── mypy.ini                # mypy type checker configuration
└── README.md
```

## Development Tools

This project uses modern Python development tools:

- **Poetry**: Dependency management and packaging
- **Ruff**: Extremely fast linter and formatter (replaces Black, isort, flake8)
- **mypy**: Static type checker with strict mode enabled
- **pytest**: Testing framework with async support
- **httpx**: HTTP client for testing FastAPI endpoints

## In-Memory Storage

This application uses in-memory storage (Python lists/dicts). Data will be lost when the application restarts. This is intentional for simplicity and is suitable for interview/demo purposes.

Check integration tests at: https://github.com/crunchloop/interview-tests

## Contact

- Martín Fernández (mfernandez@crunchloop.io)

## About Crunchloop

![crunchloop](https://s3.amazonaws.com/crunchloop.io/logo-blue.png)

We strongly believe in giving back :rocket:. Let's work together [`Get in touch`](https://crunchloop.io/#contact).

---

# Backend Setup and Documentation

## Overview

This is a FastAPI-based backend for a TodoList application that uses Redis as both a database and task queue system. The application provides a REST API for managing todo lists and items, with asynchronous task processing capabilities for bulk operations.

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.13** - Programming language
- **Redis** - In-memory data structure store (used as database and message broker)
- **RQ (Redis Queue)** - Simple Python library for queueing jobs
- **Poetry** - Dependency management and packaging
- **Pydantic** - Data validation using Python type annotations
- **Pytest** - Testing framework

## Features

- Full CRUD operations for Todo Lists
- Full CRUD operations for Todo Items
- Asynchronous task processing with Redis Queue
- Background workers for long-running operations
- Job status tracking
- Duplicate name/title validation
- Bulk operations (complete all items)
- CORS enabled for frontend integration
- Comprehensive test suite

## Prerequisites

Before running this project, ensure you have:

- **Docker** and **Docker Compose**
- **Python 3.13** (if running locally without Docker)
- **Poetry** (for dependency management)
- **Redis** (included in Docker setup)

## Redis Architecture

This project uses Redis in two distinct ways:

### 1. Redis as Database (DB 1)
- Stores all TodoLists and TodoItems as JSON
- Maintains auto-incrementing ID counters
- Provides fast key-value storage

### 2. Redis as Task Queue (DB 0)
- Manages asynchronous job queue using RQ
- Handles background task processing
- Enables non-blocking operations for expensive tasks

**Why Redis?**
- Fast in-memory operations
- Simple key-value storage for small-scale applications
- Built-in pub/sub for job queuing
- Easy to scale and deploy

## Installation

### Option 1: Docker with Dev Containers (Recommended)

This project includes a complete dev container setup for consistent development environments.

**Dev Container Configuration** (`.devcontainer/devcontainer.json`):
```json
{
    "name": "FastAPI Todo App",
    "dockerComposeFile": [
        "../docker-compose.yml",
        "docker-compose.yml"
    ],
    "service": "app",
    "workspaceFolder": "/workspaces/${localWorkspaceFolderBasename}",
    "features": {
        "ghcr.io/devcontainers/features/python:1": {
            "version": "3.13",
            "installTools": true
        },
        "ghcr.io/devcontainers/features/git:1": {
            "version": "latest"
        }
    },
    "forwardPorts": [8000],
    "postCreateCommand": "pip install poetry && poetry install",
    "customizations": {
        "vscode": {
            "extensions": [
                "ms-python.python",
                "ms-python.vscode-pylance",
                "charliermarsh.ruff",
                "ms-python.mypy-type-checker"
            ],
            "settings": {
                "python.defaultInterpreterPath": "/usr/local/bin/python",
                "python.linting.enabled": true,
                "python.formatting.provider": "none",
                "[python]": {
                    "editor.defaultFormatter": "charliermarsh.ruff",
                    "editor.formatOnSave": true,
                    "editor.codeActionsOnSave": {
                        "source.fixAll": "explicit",
                        "source.organizeImports": "explicit"
                    }
                },
                "ruff.enable": true,
                "mypy-type-checker.importStrategy": "fromEnvironment"
            }
        }
    }
}
```

**Steps to run with Docker:**

1. Open the project in VS Code
2. Install the "Dev Containers" extension
3. Press `F1` and select "Dev Containers: Reopen in Container"
4. Wait for the container to build and dependencies to install
5. The `postCreateCommand` will automatically run `poetry install`

### Option 2: Local Development

1. Install Poetry:
```bash
pip install poetry
```

2. Install dependencies:
```bash
poetry install
```

3. Ensure Redis is running locally on port 6379

## Docker Configuration

### Root docker-compose.yml
```yaml
version: '3.8'
services:
  app:
    image: mcr.microsoft.com/devcontainers/python:1-3.13-bookworm
    volumes:
      - .:/workspaces/python-interview
    ports:
      - "8000:8000"
    command: sleep infinity
    working_dir: /workspaces/python-interview
    networks:
      - fastapi-network

networks:
  fastapi-network:
    driver: bridge
```

### Dev Container docker-compose.yml
```yaml
version: '3.8'
services:
  app:
    environment:
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    volumes:
      - ..:/workspaces:cached
    command: sleep infinity
    
  redis:  
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

**Important:** The dev container setup includes Redis automatically. The app service depends on Redis and connects via `host.docker.internal:6379`.

## Project Structure

```bash
app/
├── routers/                 # API route handlers
│   ├── __init__.py
│   ├── jobs.py             # Job status endpoints
│   ├── todo_items.py       # Todo items CRUD endpoints
│   └── todo_lists.py       # Todo lists CRUD endpoints
├── services/               # Business logic layer
│   ├── __init__.py
│   ├── todo_items.py       # Todo items service
│   └── todo_lists.py       # Todo lists service (Redis storage)
├── __init__.py
├── main.py                 # FastAPI application entry point
├── models.py               # Pydantic models for validation
├── redis_config.py         # Redis connection and queue setup
└── worker.py               # Background worker for async tasks
scripts/
└── start_worker.py         # Helper script to start worker
tests/
├── __init__.py
├── test_todo_items.py      # Tests for todo items
└── test_todo_lists.py      # Tests for todo lists

Configuration Files:
├── docker-compose.yml      # Docker services configuration
├── poetry.toml             # Poetry configuration
├── poetry.lock             # Locked dependencies
├── pyproject.toml          # Project metadata and dependencies
├── .ruff.toml              # Ruff linter configuration
├── mypy.ini                # MyPy type checker configuration
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

## Running the Application

### 1. Start the FastAPI Server
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**

vscode ➜ /workspaces/python-interview (main) $ poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
INFO:     Will watch for changes in these directories: ['/workspaces/python-interview']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2940] using WatchFiles
INFO:     Started server process [3069]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

The API will be available at `http://localhost:8000`

### 2. Start the Background Worker

**Important:** The worker must be running for asynchronous operations (like "complete all") to work.
```bash
poetry run python -m app.worker
```

**Expected output:**

vscode ➜ /workspaces/python-interview (main) $ poetry run python -m app.worker
Worker started. Connecting to Redis...
Worker ready. Waiting for jobs...
15:51:27 Worker e6e648a08bf84a8e9b851cba34ef64aa: started with PID 3371, version 2.6.1
15:51:27 Worker e6e648a08bf84a8e9b851cba34ef64aa: subscribing to channel rq:pubsub:e6e648a08bf84a8e9b851cba34ef64aa
15:51:27 *** Listening on default...
15:51:27 Worker e6e648a08bf84a8e9b851cba34ef64aa: cleaning registries for queue: default

### 3. Access the API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## API Endpoints

### Health Check

GET /

Returns a simple message indicating the API is running.

### Todo Lists Endpoints

```http
GET    /api/todolists          # Get all todo lists
GET    /api/todolists/{id}     # Get a specific todo list
POST   /api/todolists          # Create a new todo list
PUT    /api/todolists/{id}     # Update a todo list
DELETE /api/todolists/{id}     # Delete a todo list
```

### Todo Items Endpoints

```http
GET    /api/todolists/{list_id}/items                     # Get all items in a list
GET    /api/todolists/{list_id}/items/{item_id}          # Get a specific item
POST   /api/todolists/{list_id}/items                    # Create a new item
PUT    /api/todolists/{list_id}/items/{item_id}          # Update an item
PATCH  /api/todolists/{list_id}/items/{item_id}/toggle   # Toggle item completion
DELETE /api/todolists/{list_id}/items/{item_id}          # Delete an item
POST   /api/todolists/{list_id}/items/complete-all       # Complete all items (async)
```

### Job Status Endpoints

GET /api/jobs/{job_id}             # Check status of an async job

## Asynchronous Task Processing

### How "Complete All" Works

The "complete all" operation is implemented as an asynchronous task to handle large lists efficiently:

#### 1. Request Flow

Client → POST /api/todolists/{id}/items/complete-all
↓
Enqueue job to Redis Queue
↓
Return job_id immediately (202 Accepted)
↓
Background Worker processes job
↓
Update all items in Redis DB

#### 2. Components

**Router (`routers/todo_items.py`):**
```python
@router.post("/complete-all", status_code=202)
async def complete_all_async(todo_list_id: int) -> dict:
    """Queues the task and responds immediately."""
    job_id = enqueue_complete_all(todo_list_id)
    return {
        "message": "queued job",
        "job_id": job_id,
        "todo_list_id": todo_list_id,
        "check_status": f"/api/jobs/{job_id}",
    }
```

**Redis Configuration (`redis_config.py`):**
```python
# Redis connection for queue (DB 0)
redis_conn = redis.Redis(host="host.docker.internal", port=6379, db=0)
queue = Queue(connection=redis_conn)

def enqueue_complete_all(todo_list_id: int) -> str:
    """Enqueues the job and returns job ID."""
    from app.worker import complete_all_task
    job = queue.enqueue(complete_all_task, todo_list_id)
    return job.id
```

**Worker (`worker.py`):**
```python
def complete_all_task(todo_list_id: int) -> dict:
    """Task that the worker executes."""
    service = get_todo_item_service()
    todo_list_service = get_todo_list_service()
    
    todo_list = todo_list_service.get(todo_list_id)
    if not todo_list:
        return {"error": "List not found"}
    
    completed_count = 0
    for i, item in enumerate(todo_list.items):
        if not item.completed:
            todo_list.items[i] = item.__class__(
                id=item.id,
                title=item.title,
                description=item.description,
                completed=True,
            )
            completed_count += 1
    
    if completed_count > 0:
        todo_list_service.save(todo_list)
    
    return {
        "completed": completed_count,
        "message": f"Completed {completed_count} tasks"
    }
```

#### 3. Checking Job Status

After receiving a job_id, clients can check the status:
```bash
GET /api/jobs/{job_id}
```

Response:
```json
{
    "id": "abc123",
    "status": "finished",
    "result": {
        "completed": 5,
        "message": "Completed 5 tasks"
    },
    "error": null
}
```

**Job Statuses:**
- `queued` - Job is waiting to be processed
- `started` - Job is currently being processed
- `finished` - Job completed successfully
- `failed` - Job failed with an error

### Why Use Async Processing?

1. **Non-blocking:** API responds immediately, doesn't wait for task completion
2. **Scalability:** Can handle large lists without timeout issues
3. **Better UX:** Frontend can show progress or poll for status
4. **Resource efficiency:** Worker can process jobs in background
5. **Error handling:** Failed jobs can be retried or logged

## Data Models

### TodoList
```python
class TodoList(BaseModel):
    id: int
    name: str
    items: list[TodoItem] = []
```

### TodoItem
```python
class TodoItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
```

### Create/Update DTOs
```python
class TodoListCreate(BaseModel):
    name: str  # min_length=1

class TodoListUpdate(BaseModel):
    name: str  # min_length=1

class TodoItemCreate(BaseModel):
    title: str  # min_length=1
    description: Optional[str] = None
    completed: bool = False

class TodoItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
```

## Business Logic & Validation

### TodoList Service

**Features:**
- Duplicate name validation (case-insensitive)
- Auto-incrementing IDs using Redis counters
- JSON serialization/deserialization for Redis storage
- Cascade operations (items included with lists)

**Redis Keys:**
- `todolist:{id}` - Stores serialized TodoList
- `todolist:next_id` - Global counter for list IDs

### TodoItem Service

**Features:**
- Duplicate title validation within each list (case-insensitive)
- Per-list ID generation
- Toggle completion status
- Bulk complete operation

**Redis Keys:**
- `todoitem:{list_id}:next_id` - Counter for items in specific list
- Items are stored within their parent TodoList

## Testing

The project includes a comprehensive test suite using pytest.

### Running Tests

**Run all tests:**
```bash
poetry run pytest
```

**Run specific test file:**
```bash
poetry run pytest tests/test_todo_lists.py -v
poetry run pytest tests/test_todo_items.py -v
```

**Run tests with coverage:**
```bash
poetry run pytest --cov=app --cov-report=html
```

**Run tests in watch mode:**
```bash
poetry run pytest-watch
```

**Run tests with verbose output:**
```bash
poetry run pytest -v
```

### Test Coverage

The test suite includes comprehensive unit tests using mocked services:

**TodoList Tests (`test_todo_lists.py`):**
- **GET /api/todolists** - Returns all todo lists
- **GET /api/todolists** - Returns empty list when no todos exist
- **GET /api/todolists/{id}** - Returns a specific todo list by ID
- **GET /api/todolists/{id}** - Returns 404 when todo list not found
- **POST /api/todolists** - Creates new todo list successfully
- **POST /api/todolists** - Validates required fields (422 error)
- **POST /api/todolists** - Validates name is not empty (422 error)
- **PUT /api/todolists/{id}** - Updates existing todo list
- **PUT /api/todolists/{id}** - Returns 404 when todo list not found
- **PUT /api/todolists/{id}** - Validates required fields (422 error)
- **DELETE /api/todolists/{id}** - Deletes existing todo list (204 response)
- **DELETE /api/todolists/{id}** - Returns 404 when todo list not found

**TodoItem Tests (`test_todo_items.py`):**
- **GET /api/todolists/{id}/items** - Returns all items from a list
- **GET /api/todolists/{id}/items/{item_id}** - Returns a specific item
- **GET /api/todolists/{id}/items/{item_id}** - Returns 404 when item not found
- **POST /api/todolists/{id}/items** - Creates new item successfully
- **POST /api/todolists/{id}/items** - Rejects duplicate titles (400 error)
- **PUT /api/todolists/{id}/items/{item_id}** - Updates existing item
- **PUT /api/todolists/{id}/items/{item_id}** - Rejects duplicate title of another item (400 error)
- **PATCH /api/todolists/{id}/items/{item_id}/toggle** - Toggles completion status
- **DELETE /api/todolists/{id}/items/{item_id}** - Deletes an item (204 response)
- **POST /api/todolists/{id}/items/complete-all** - Enqueues async job (202 response)

**Testing Strategy:**
- Uses `pytest` fixtures for test client and mocked services
- Mocks `TodoListService` and `TodoItemService` to isolate endpoint logic
- Tests HTTP status codes, response structure, and service method calls
- Covers success cases, validation errors, and not found scenarios
- Validates FastAPI's automatic request validation (422 errors)

## Redis Configuration Details

### Connection Settings
```python
# Redis for data storage (DB 1)
redis_conn = Redis(
    host="host.docker.internal",  # Docker host
    port=6379,
    db=1,  # Database 1 for data
    decode_responses=True  # Automatic string decoding
)

# Redis for job queue (DB 0)
redis_conn = Redis(
    host="host.docker.internal",
    port=6379,
    db=0  # Database 0 for queue
)
```

**Why `host.docker.internal`?**
- Allows containers to connect to services on the host machine
- Redis runs in a separate container, accessible via Docker networking
- Alternative: Use service name `redis` if both services are in same compose file

### Redis Database Separation

- **DB 0:** Job queue and worker communication
- **DB 1:** Application data (TodoLists and TodoItems)

This separation prevents queue operations from interfering with data storage.

## CORS Configuration

The API is configured to accept requests from any origin:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production Note:** Restrict `allow_origins` to specific domains in production.

## Development Tools

### Code Quality Tools

- **Ruff:** Fast Python linter and formatter
- **MyPy:** Static type checker
- **Pytest:** Testing framework

### VS Code Extensions

The dev container automatically installs:
- Python extension
- Pylance (language server)
- Ruff (linting/formatting)
- MyPy type checker

### Poetry Commands
```bash
# Add a new dependency
poetry add package-name

# Add a dev dependency
poetry add --group dev package-name

# Update dependencies
poetry update

# Show installed packages
poetry show

# Run a command in the virtual environment
poetry run python script.py
```

## Troubleshooting

### Redis Connection Issues

**Problem:** `ConnectionError: Error 111 connecting to redis:6379`

**Solutions:**
1. Ensure Redis container is running: `docker ps`
2. Check Redis is accessible: `redis-cli ping`
3. Verify `host.docker.internal` resolves correctly
4. Check firewall settings

### Worker Not Processing Jobs

**Problem:** Jobs stay in "queued" status

**Solutions:**
1. Ensure worker is running: `poetry run python -m app.worker`
2. Check worker logs for errors
3. Verify Redis connection in worker
4. Restart worker process

### Port Already in Use

**Problem:** Port 8000 is already in use

**Solutions:**
1. Find process using port: `lsof -i :8000`
2. Kill the process or use a different port
3. Change port in uvicorn command: `--port 8001`

### Poetry Install Fails

**Problem:** Dependencies fail to install

**Solutions:**
1. Update Poetry: `pip install --upgrade poetry`
2. Clear cache: `poetry cache clear pypi --all`
3. Delete `poetry.lock` and reinstall
4. Check Python version: `python --version` (should be 3.13)

### Tests Failing

**Problem:** Tests fail with Redis errors

**Solutions:**
1. Ensure Redis is running and accessible
2. Clear Redis data: `redis-cli FLUSHALL`
3. Check test isolation (tests should clean up after themselves)
4. Run tests individually to identify issues

## Environment Variables

The application uses minimal environment configuration:
```bash
REDIS_URL=redis://redis:6379  # Set in docker-compose
```

For local development without Docker, you may need to adjust Redis connection strings in:
- `app/services/todo_lists.py`
- `app/services/todo_items.py`
- `app/redis_config.py`
- `app/worker.py`

## Production Considerations

Before deploying to production:

1. **Security:**
   - Restrict CORS origins
   - Add authentication/authorization
   - Use environment variables for sensitive config
   - Enable HTTPS

2. **Redis:**
   - Use managed Redis service (AWS ElastiCache, Redis Cloud)
   - Enable Redis persistence
   - Configure password authentication
   - Set up Redis clustering for high availability

3. **Workers:**
   - Run multiple worker instances
   - Use supervisor or systemd for process management
   - Monitor worker health
   - Implement retry logic for failed jobs

4. **Monitoring:**
   - Add logging (structured logging)
   - Set up error tracking (Sentry)
   - Monitor Redis memory usage
   - Track API performance metrics

## Contributing

When contributing to this project:

1. Follow PEP 8 style guide (enforced by Ruff)
2. Add type hints to all functions
3. Write tests for new features
4. Update documentation as needed
5. Run linter and tests before committing:
```bash
   poetry run ruff check .
   poetry run mypy .
   poetry run pytest
```

## API Response Examples

### Create Todo List

**Request:**
```bash
POST /api/todolists
Content-Type: application/json

{
    "name": "Shopping List"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "name": "Shopping List",
    "items": []
}
```

### Create Todo Item

**Request:**
```bash
POST /api/todolists/1/items
Content-Type: application/json

{
    "title": "Buy milk",
    "description": "2 gallons of whole milk",
    "completed": false
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "title": "Buy milk",
    "description": "2 gallons of whole milk",
    "completed": false
}
```

### Complete All Items (Async)

**Request:**
```bash
POST /api/todolists/1/items/complete-all
```

**Response (202 Accepted):**
```json
{
    "message": "queued job",
    "job_id": "550e8400-e29b-41d4-a716-446655440000",
    "todo_list_id": 1,
    "check_status": "/api/jobs/550e8400-e29b-41d4-a716-446655440000"
}
```

## Quick Start Summary

1. **Open in Dev Container** (VS Code)
2. **Start FastAPI:** `poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
3. **Start Worker:** `poetry run python -m app.worker`
4. **Visit:** http://localhost:8000/docs
5. **Run Tests:** `poetry run pytest`


Your backend is now ready to serve the React frontend! 🚀

