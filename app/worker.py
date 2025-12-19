"""Worker for processing async tasks."""

from redis import Redis
from rq import Queue, Worker

from app.services.todo_items import get_todo_item_service
from app.services.todo_lists import get_todo_list_service


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

    # save in redis
    if completed_count > 0:
        todo_list_service.save(todo_list)

    return {"completed": completed_count, "message": f"Completadas {completed_count} tareas"}


if __name__ == "__main__":
    print("Worker started. Connecting to Redis...")
    redis_conn = Redis(host="host.docker.internal", port=6379, db=0)
    queue = Queue(connection=redis_conn)
    worker = Worker([queue])
    print("Worker ready. Waiting for jobs...")
    worker.work()
