"""Unit tests for TodoItem API endpoints."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import TodoItem
from app.services.todo_items import get_todo_item_service


@pytest.fixture
def mock_item_service() -> Generator[MagicMock, None, None]:
    """Mock TodoItemService para testing."""
    mock = MagicMock()
    app.dependency_overrides[get_todo_item_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


@pytest.fixture
def client() -> TestClient:
    """Test client para FastAPI."""
    return TestClient(app)


class TestTodoItems:
    """Tests concisos para endpoints de items."""

    def test_index_returns_items(self, client: TestClient, mock_item_service: MagicMock) -> None:
        """GET /items - Retorna todos los items de una lista."""
        mock_item_service.get_all.return_value = [
            TodoItem(id=1, title="Tarea 1", completed=False),
            TodoItem(id=2, title="Tarea 2", completed=True),
        ]

        response = client.get("/api/todolists/1/items")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Tarea 1"
        mock_item_service.get_all.assert_called_once_with(1)

    def test_show_returns_single_item(
        self, client: TestClient, mock_item_service: MagicMock
    ) -> None:
        """GET /items/{id} - Returns a specific item."""
        mock_item_service.get.return_value = TodoItem(id=1, title="Tarea", completed=False)

        response = client.get("/api/todolists/1/items/1")

        assert response.status_code == 200
        assert response.json()["title"] == "Tarea"
        mock_item_service.get.assert_called_once_with(1, 1)

    def test_show_returns_404_when_not_found(
        self, client: TestClient, mock_item_service: MagicMock
    ) -> None:
        """GET /items/{id} - Returns 404 when it does not exist."""
        mock_item_service.get.return_value = None

        response = client.get("/api/todolists/1/items/999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_create_item_success(self, client: TestClient, mock_item_service: MagicMock) -> None:
        """POST /items - Create a new item."""
        mock_item_service.get_all.return_value = []
        mock_item_service.create.return_value = TodoItem(id=1, title="Nueva tarea", completed=False)

        response = client.post(
            "/api/todolists/1/items", json={"title": "Nueva tarea", "completed": False}
        )

        assert response.status_code == 201
        assert response.json()["title"] == "Nueva tarea"
        mock_item_service.create.assert_called_once()

    def test_create_rejects_duplicate_title(
        self, client: TestClient, mock_item_service: MagicMock
    ) -> None:
        """POST /items - Reject duplicate titles."""
        existing_item = TodoItem(id=1, title="Tarea Existente", completed=False)
        mock_item_service.get_all.return_value = [existing_item]

        response = client.post(
            "/api/todolists/1/items", json={"title": "Tarea Existente", "completed": False}
        )

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()
        mock_item_service.create.assert_not_called()

    def test_update_item_success(self, client: TestClient, mock_item_service: MagicMock) -> None:
        """PUT /items/{id} - Update an existing item."""
        current_item = TodoItem(id=1, title="Viejo", completed=False)
        updated_item = TodoItem(id=1, title="Nuevo", completed=True)

        mock_item_service.get.return_value = current_item
        mock_item_service.get_all.return_value = [current_item]  # Solo este item existe
        mock_item_service.update.return_value = updated_item

        response = client.put(
            "/api/todolists/1/items/1", json={"title": "Nuevo", "completed": True}
        )

        assert response.status_code == 200
        assert response.json()["title"] == "Nuevo"
        assert response.json()["completed"] is True

    def test_update_rejects_duplicate_title(
        self, client: TestClient, mock_item_service: MagicMock
    ) -> None:
        """PUT /items/{id} - Reject duplicate title of another item."""
        current_item = TodoItem(id=1, title="Actual", completed=False)
        other_item = TodoItem(id=2, title="Otro", completed=True)

        mock_item_service.get.return_value = current_item
        mock_item_service.get_all.return_value = [current_item, other_item]

        response = client.put("/api/todolists/1/items/1", json={"title": "Otro", "completed": True})

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()
        mock_item_service.update.assert_not_called()

    def test_toggle_item_completion(self, client: TestClient, mock_item_service: MagicMock) -> None:
        """PATCH /items/{id}/toggle - Change completed status."""
        toggled_item = TodoItem(id=1, title="Tarea", completed=True)
        mock_item_service.toggle.return_value = toggled_item

        response = client.patch("/api/todolists/1/items/1/toggle")

        assert response.status_code == 200
        assert response.json()["completed"] is True
        mock_item_service.toggle.assert_called_once_with(1, 1)

    def test_delete_item_success(self, client: TestClient, mock_item_service: MagicMock) -> None:
        """DELETE /items/{id} - Delete an item."""
        mock_item_service.delete.return_value = True

        response = client.delete("/api/todolists/1/items/1")

        assert response.status_code == 204
        mock_item_service.delete.assert_called_once_with(1, 1)

    def test_complete_all_async_enqueues_job(self, client: TestClient) -> None:
        """POST /items/complete-all - Queue asynchronous work."""
        with patch("app.routers.todo_items.enqueue_complete_all") as mock_enqueue:
            mock_enqueue.return_value = "job-123"

            response = client.post("/api/todolists/1/items/complete-all")

            assert response.status_code == 202
            data = response.json()
            assert data["message"] == "queued job"
            assert data["job_id"] == "job-123"
            mock_enqueue.assert_called_once_with(1)
