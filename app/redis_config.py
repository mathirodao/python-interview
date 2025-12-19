"""Redis configuration for async task queue."""

import redis
from rq import Queue

# Redis connection
redis_conn = redis.Redis(host="host.docker.internal", port=6379, db=0)
queue = Queue(connection=redis_conn)


def enqueue_complete_all(todo_list_id: int) -> str:
    """Encuela el trabajo y devuelve ID."""
    from app.worker import complete_all_task

    job = queue.enqueue(complete_all_task, todo_list_id)
    return job.id
