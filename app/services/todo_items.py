"""TodoItem service for managing items within TodoLists."""

from typing import Optional

from redis import Redis

from app.models import TodoItem, TodoItemCreate, TodoItemUpdate
from app.services.todo_lists import get_todo_list_service

# Connection to Redis for item counter (DB 1)
redis_conn = Redis(host="host.docker.internal", port=6379, db=1, decode_responses=True)


class TodoItemService:
    """Service for managing TodoItems within TodoLists."""

    def __init__(self) -> None:
        """Initialize the service."""
        if not redis_conn.exists("todoitem:next_id"):
            redis_conn.set("todoitem:next_id", 1)

    def _get_next_item_id(self, todo_list_id: int) -> int:
        """Obtiene ID único para items en una lista específica."""
        key = f"todoitem:{todo_list_id}:next_id"
        if not redis_conn.exists(key):
            redis_conn.set(key, 1)
        return redis_conn.incr(key)

    def _title_exists_in_list(
        self, todo_list_id: int, title: str, exclude_item_id: Optional[int] = None
    ) -> bool:
        """
        Verifica si ya existe un item con ese título en la lista (case-insensitive).

        Args:
            todo_list_id: ID de la lista
            title: Título a verificar
            exclude_item_id: ID of the item to exclude from the search (for updates)

        Returns:
            True if the title already exists, False if not
        """
        items = self.get_all(todo_list_id)
        if items is None:
            return False

        title_lower = title.strip().lower()

        for item in items:
            if exclude_item_id is not None and item.id == exclude_item_id:
                continue

            if item.title.lower() == title_lower:
                return True

        return False

    def get_all(self, todo_list_id: int) -> Optional[list[TodoItem]]:
        """Get all items from a todo list."""
        todo_list_service = get_todo_list_service()
        todo_list = todo_list_service.get(todo_list_id)
        if todo_list is None:
            return None
        return todo_list.items

    def get(self, todo_list_id: int, item_id: int) -> Optional[TodoItem]:
        """Get a specific item from a todo list."""
        items = self.get_all(todo_list_id)
        if items is None:
            return None
        for item in items:
            if item.id == item_id:
                return item
        return None

    def create(self, todo_list_id: int, item_data: TodoItemCreate) -> Optional[TodoItem]:
        """
        Create a new item in a todo list.

        Raises:
            ValueError: Si el título ya existe en la lista
        """
        todo_list_service = get_todo_list_service()
        todo_list = todo_list_service.get(todo_list_id)
        if todo_list is None:
            return None

        # Validate duplicate title in list
        if self._title_exists_in_list(todo_list_id, item_data.title):
            raise ValueError(f"A task with title '{item_data.title}' already exists in this list")

        # Create new item with Redis ID
        new_item = TodoItem(
            id=self._get_next_item_id(todo_list_id),
            title=item_data.title,
            description=item_data.description,
            completed=item_data.completed,
        )

        # add to list
        todo_list.items.append(new_item)

        # save in redis
        todo_list_service.save(todo_list)
        return new_item

    def update(
        self, todo_list_id: int, item_id: int, item_data: TodoItemUpdate
    ) -> Optional[TodoItem]:
        """
        Update an existing item.

        Raises:
            ValueError: If the title already exists in the list
        """
        todo_list_service = get_todo_list_service()
        todo_list = todo_list_service.get(todo_list_id)
        if todo_list is None:
            return None

        # Buscar el item
        for i, item in enumerate(todo_list.items):
            if item.id == item_id:
                new_title = item_data.title if item_data.title is not None else item.title

                # validate title
                if new_title != item.title:
                    if self._title_exists_in_list(todo_list_id, new_title, exclude_item_id=item_id):
                        raise ValueError(
                            f"A task with title '{new_title}' already exists in this list"
                        )

                # Update only provided fields
                updated_item = TodoItem(
                    id=item.id,
                    title=new_title,
                    description=item_data.description
                    if item_data.description is not None
                    else item.description,
                    completed=item_data.completed
                    if item_data.completed is not None
                    else item.completed,
                )
                # replace in list
                todo_list.items[i] = updated_item

                # save in redis
                todo_list_service.save(todo_list)
                return updated_item

        return None

    def toggle(self, todo_list_id: int, item_id: int) -> Optional[TodoItem]:
        """Toggle the completion status of an item."""
        todo_list_service = get_todo_list_service()
        todo_list = todo_list_service.get(todo_list_id)
        if todo_list is None:
            return None

        # search item
        for i, item in enumerate(todo_list.items):
            if item.id == item_id:
                # Create updated item
                updated_item = TodoItem(
                    id=item.id,
                    title=item.title,
                    description=item.description,
                    completed=not item.completed,
                )
                # Replace
                todo_list.items[i] = updated_item

                # save in redis
                todo_list_service.save(todo_list)
                return updated_item

        return None

    def complete_all(self, todo_list_id: int) -> Optional[int]:
        """Mark all incomplete items in a todo list as completed."""
        todo_list_service = get_todo_list_service()
        todo_list = todo_list_service.get(todo_list_id)
        if todo_list is None:
            return None

        completed_count = 0
        for i, item in enumerate(todo_list.items):
            if not item.completed:
                updated_item = TodoItem(
                    id=item.id,
                    title=item.title,
                    description=item.description,
                    completed=True,
                )
                todo_list.items[i] = updated_item
                completed_count += 1

        if completed_count > 0:
            # save in redis
            todo_list_service.save(todo_list)

        return completed_count

    def delete(self, todo_list_id: int, item_id: int) -> bool:
        """Delete an item from a todo list."""
        todo_list_service = get_todo_list_service()
        todo_list = todo_list_service.get(todo_list_id)
        if todo_list is None:
            return False

        # search and delete item
        for i, item in enumerate(todo_list.items):
            if item.id == item_id:
                todo_list.items.pop(i)
                # save in redis
                todo_list_service.save(todo_list)
                return True

        return False


# Global singleton instance
_todo_item_service = None


def get_todo_item_service():
    global _todo_item_service
    if _todo_item_service is None:
        _todo_item_service = TodoItemService()
    return _todo_item_service
