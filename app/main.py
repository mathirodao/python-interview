"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import jobs, todo_items, todo_lists

# Create FastAPI application instance
app = FastAPI(
    title="TodoList API",
    description="A simple Todo List API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(todo_lists.router)
app.include_router(todo_items.router)
app.include_router(jobs.router)


@app.get("/", tags=["health"])
async def root() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Simple message indicating the API is running
    """
    return {"message": "TodoList API is running"}
