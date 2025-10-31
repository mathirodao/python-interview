"""FastAPI application entry point."""

from fastapi import FastAPI

from app.routers import todo_lists

# Create FastAPI application instance
app = FastAPI(
    title="TodoList API",
    description="A simple Todo List API",
    version="1.0.0",
)

# Include routers
app.include_router(todo_lists.router)


@app.get("/", tags=["health"])
async def root() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Simple message indicating the API is running
    """
    return {"message": "TodoList API is running"}
