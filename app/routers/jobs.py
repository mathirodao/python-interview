from fastapi import APIRouter, HTTPException
from redis import Redis
from rq.job import Job

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.get("/{job_id}")
def get_job_status(job_id: str):
    """View status of a job."""
    try:
        redis_conn = Redis(host="host.docker.internal", port=6379, db=0)
        job = Job.fetch(job_id, connection=redis_conn)

        return {
            "id": job.id,
            "status": job.get_status(),
            "result": job.result,
            "error": job.exc_info,
        }
    except:
        raise HTTPException(404, "Job not found")
