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
