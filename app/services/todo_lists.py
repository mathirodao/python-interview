"""TodoList service with Redis storage."""

import json
from typing import List, Optional

from redis import Redis

from app.models import TodoItem, TodoList, TodoListCreate, TodoListUpdate

# Connecting to Redis (DB 1 for data, different from queue in DB 0)
redis_conn = Redis(host="host.docker.internal", port=6379, db=1, decode_responses=True)


class TodoListService:
    """Service for managing TodoLists with Redis storage."""

    def __init__(self) -> None:
        """Initialize the service."""
        # Initialize ID counter if it does not exist
        if not redis_conn.exists("todolist:next_id"):
            redis_conn.set("todolist:next_id", 1)

    def _get_next_id(self) -> int:
        """Gets and increments the next ID."""
        return redis_conn.incr("todolist:next_id")

    def _get_key(self, todo_list_id: int) -> str:
        return f"todolist:{todo_list_id}"

    def _serialize(self, todo_list: TodoList) -> str:
        """Convert TodoList to JSON for Redis."""
        return json.dumps(
            {
                "id": todo_list.id,
                "name": todo_list.name,
                "items": [item.model_dump() for item in todo_list.items],
            }
        )

    def _deserialize(self, data: str) -> TodoList:
        """Convierte JSON de Redis a TodoList."""
        obj = json.loads(data)
        # Rebuild items as TodoItem objects
        items = [TodoItem(**item) for item in obj["items"]]
        return TodoList(id=obj["id"], name=obj["name"], items=items)

    def _name_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """
        Checks if a list with that name already exists (case-insensitive).

        Args:
            name: Name to verify
            exclude_id: ID to exclude from the search (for updates)

        Returns:
            True if the name already exists, False if not
        """
        all_lists = self.all()
        name_lower = name.strip().lower()

        for todo_list in all_lists:
            # If we are updating, exclude the item that is being edited
            if exclude_id is not None and todo_list.id == exclude_id:
                continue

            if todo_list.name.lower() == name_lower:
                return True

        return False

    def all(self) -> List[TodoList]:
        """Get all todo lists."""
        keys = redis_conn.keys("todolist:*")
        # Exclude counter key
        keys = [key for key in keys if key != "todolist:next_id"]

        result = []
        for key in keys:
            data = redis_conn.get(key)
            if data:
                result.append(self._deserialize(data))

        return result

    def get(self, todo_list_id: int) -> Optional[TodoList]:
        """Get a specific todo list by ID."""
        key = self._get_key(todo_list_id)
        data = redis_conn.get(key)

        if not data:
            return None

        return self._deserialize(data)

    def create(self, todo_list_data: TodoListCreate) -> TodoList:
        """
        Create a new todo list.

        Raises:
            ValueError: If name already exists
        """
        # Validate duplicate name
        if self._name_exists(todo_list_data.name):
            raise ValueError(f"A list with the name '{todo_list_data.name} already exists'")

        new_id = self._get_next_id()
        new_todo_list = TodoList(
            id=new_id,
            name=todo_list_data.name,
            items=[],
        )

        # save in redis
        key = self._get_key(new_id)
        redis_conn.set(key, self._serialize(new_todo_list))

        return new_todo_list

    def update(self, todo_list_id: int, todo_list_data: TodoListUpdate) -> Optional[TodoList]:
        """
        Update an existing todo list.

        Raises:
            ValueError: If name already exists
        """
        existing = self.get(todo_list_id)
        if not existing:
            return None

        # Validate duplicate name (excluding current one)
        if self._name_exists(todo_list_data.name, exclude_id=todo_list_id):
            raise ValueError(f"A list with the name '{todo_list_data.name} already exists'")

        updated = TodoList(
            id=todo_list_id,
            name=todo_list_data.name,
            items=existing.items,
        )

        # save in redis
        key = self._get_key(todo_list_id)
        redis_conn.set(key, self._serialize(updated))

        return updated

    def delete(self, todo_list_id: int) -> bool:
        """Delete a todo list by ID."""
        key = self._get_key(todo_list_id)
        return redis_conn.delete(key) > 0

    def save(self, todo_list: TodoList) -> None:
        """Guarda una TodoList en Redis (para usar desde todo_items.py)."""
        key = self._get_key(todo_list.id)
        redis_conn.set(key, self._serialize(todo_list))


# Global singleton instance
_todo_list_service: Optional[TodoListService] = None


def get_todo_list_service() -> TodoListService:
    """Get or create the singleton TodoListService instance."""
    global _todo_list_service
    if _todo_list_service is None:
        _todo_list_service = TodoListService()
    return _todo_list_service
