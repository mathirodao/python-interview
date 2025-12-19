"""Pydantic models for TodoList API."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ===== TodoItem Models =====
class TodoItemBase(BaseModel):
    """Base TodoItem model with common attributes."""

    title: str = Field(..., min_length=1, description="Title of the todo item")
    description: Optional[str] = Field(default=None, description="Optional description")
    completed: bool = Field(default=False, description="Completion status")


class TodoItemCreate(TodoItemBase):
    """Model for creating a new TodoList."""

    pass


class TodoItemUpdate(BaseModel):
    """Model for updating a TodoItem."""

    title: Optional[str] = Field(None, min_length=1, description="Title of the todo item")
    description: Optional[str] = Field(None, description="Optional description")
    completed: Optional[bool] = Field(None, description="Completion status")


class TodoItem(TodoItemBase):
    """TodoList model with all attributes including ID."""

    id: int = Field(..., description="Unique identifier for item")

    model_config = ConfigDict(from_attributes=True)


# ===== TodoList Models =====
class TodoListBase(BaseModel):
    """Base TodoList model with common attributes."""

    name: str = Field(..., min_length=1, description="Name of the todo list")


class TodoListCreate(TodoListBase):
    """Model for creating a new TodoList."""

    pass


class TodoListUpdate(TodoListBase):
    """Model for updating an existing TodoList."""

    pass


class TodoList(TodoListBase):
    """TodoList model with all attributes including ID."""

    id: int = Field(..., description="Unique identifier for the todo list")
    items: list[TodoItem] = Field(default_factory=list, description="Name of the todo item")

    model_config = ConfigDict(from_attributes=True)
