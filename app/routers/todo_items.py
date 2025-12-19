"""TodoItem API router with CRUD endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.models import TodoItem, TodoItemCreate, TodoItemUpdate
from app.redis_config import enqueue_complete_all
from app.services.todo_items import TodoItemService, get_todo_item_service

router = APIRouter(prefix="/api/todolists/{todo_list_id}/items", tags=["items"])


@router.get("", response_model=list[TodoItem], status_code=status.HTTP_200_OK)
async def index(
    todo_list_id: int,
    service: Annotated[TodoItemService, Depends(get_todo_item_service)],
) -> list[TodoItem]:
    """Get all items from a todo list."""
    items = service.get_all(todo_list_id)
    if items is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TodoList with id {todo_list_id} not found",
        )
    return items


@router.get("/{item_id}", response_model=TodoItem, status_code=status.HTTP_200_OK)
async def show(
    todo_list_id: int,
    item_id: int,
    service: Annotated[TodoItemService, Depends(get_todo_item_service)],
) -> TodoItem:
    """Get a specific item from a todo list."""
    item = service.get(todo_list_id, item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found in TodoList {todo_list_id}",
        )
    return item


@router.post("", response_model=TodoItem, status_code=status.HTTP_201_CREATED)
async def create(
    todo_list_id: int,
    item_data: TodoItemCreate,
    service: Annotated[TodoItemService, Depends(get_todo_item_service)],
) -> TodoItem:
    """Create a new item in a todo list."""
    existing_items = service.get_all(todo_list_id)
    if existing_items:
        for item in existing_items:
            if item.title.lower() == item_data.title.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"A task with title '{item_data.title}' already exists in this list",
                )

    item = service.create(todo_list_id, item_data)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TodoList with id {todo_list_id} not found",
        )
    return item


@router.put("/{item_id}", response_model=TodoItem, status_code=status.HTTP_200_OK)
async def update(
    todo_list_id: int,
    item_id: int,
    item_data: TodoItemUpdate,
    service: Annotated[TodoItemService, Depends(get_todo_item_service)],
) -> TodoItem:
    """Update an existing item."""
    current_item = service.get(todo_list_id, item_id)
    if current_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found in TodoList {todo_list_id}",
        )

    existing_items = service.get_all(todo_list_id)
    if existing_items:
        for item in existing_items:
            if item.id != item_id and item.title.lower() == item_data.title.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"A task with title '{item_data.title}' already exists in this list",
                )

    item = service.update(todo_list_id, item_id, item_data)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found in TodoList {todo_list_id}",
        )
    return item


@router.patch("/{item_id}/toggle", response_model=TodoItem, status_code=status.HTTP_200_OK)
async def toggle(
    todo_list_id: int,
    item_id: int,
    service: Annotated[TodoItemService, Depends(get_todo_item_service)],
) -> TodoItem:
    """Toggle the completion status of an item."""
    item = service.toggle(todo_list_id, item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found in TodoList {todo_list_id}",
        )
    return item


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


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    todo_list_id: int,
    item_id: int,
    service: Annotated[TodoItemService, Depends(get_todo_item_service)],
) -> None:
    """Delete an item from a todo list."""
    deleted = service.delete(todo_list_id, item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found in TodoList {todo_list_id}",
        )
