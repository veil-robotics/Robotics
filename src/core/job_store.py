from __future__ import annotations

from dataclasses import replace
from threading import Lock
from typing import Dict, Optional

from .models import AnonymizationJob, JobStatus


class InMemoryJobStore:
    def __init__(self) -> None:
        self._jobs: Dict[str, AnonymizationJob] = {}
        self._lock = Lock()

    def create(self, job: AnonymizationJob) -> None:
        with self._lock:
            self._jobs[job.id] = job

    def get(self, job_id: str) -> Optional[AnonymizationJob]:
        with self._lock:
            return self._jobs.get(job_id)

    def update_status(
        self,
        job_id: str,
        status: JobStatus,
        failure_reason: Optional[str] = None,
    ) -> Optional[AnonymizationJob]:
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return None
            updated = replace(job, status=status, failure_reason=failure_reason)
            self._jobs[job_id] = updated
            return updated
