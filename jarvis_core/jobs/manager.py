from concurrent.futures import ThreadPoolExecutor
from time import time
from threading import Lock

from .job import Job


class JobManager:
    def __init__(self):
        self.jobs: dict[str, Job] = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.lock = Lock()

    def submit(self, job_name: str, fn, *args, **kwargs) -> Job:
        job = Job(name=job_name)

        with self.lock:
            self.jobs[job.id] = job

        self.executor.submit(self._run, job.id, fn, args, kwargs)
        return job

    def _run(self, job_id: str, fn, args, kwargs):
        job = self.get(job_id)
        if not job:
            return

        job.status = "running"
        job.started = time()
        job.progress = 1.0
        job.message = "Started"

        try:
            result = fn(*args, **kwargs)
            job.result = result
            job.progress = 100.0
            job.status = "completed"
            job.message = "Completed"
        except Exception as e:
            job.status = "failed"
            job.error = str(e)
            job.message = str(e)
        finally:
            job.finished = time()

    def update(self, job_id: str, progress: float | None = None, message: str | None = None):
        job = self.get(job_id)
        if not job:
            return None

        if progress is not None:
            job.progress = max(0.0, min(100.0, float(progress)))

        if message is not None:
            job.message = message

        return job

    def cancel(self, job_id: str):
        job = self.get(job_id)
        if not job:
            return None

        if job.status in {"completed", "failed", "cancelled"}:
            return job

        job.status = "cancelled"
        job.finished = time()
        job.message = "Cancelled"
        return job

    def all(self):
        with self.lock:
            return [job.to_dict() for job in self.jobs.values()]

    def get(self, job_id: str):
        with self.lock:
            return self.jobs.get(job_id)

    def get_dict(self, job_id: str):
        job = self.get(job_id)
        return job.to_dict() if job else None
