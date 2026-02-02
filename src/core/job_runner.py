from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from .job_store import InMemoryJobStore
from .models import AnonymizationJob, JobStatus, ProtectionMode, VideoAsset
from .pipeline import anonymize_video
from .validators import validate_input_path, validate_output_path


class JobRunner:
    def __init__(self, store: InMemoryJobStore) -> None:
        self._store = store

    def run_job(
        self, source_path: Path, mode: ProtectionMode, output_path: Path, summary_path: Path
    ) -> AnonymizationJob:
        job_id = str(uuid4())
        validate_input_path(source_path)
        validate_output_path(output_path)
        asset = VideoAsset(id=str(uuid4()), source_path=source_path, format=source_path.suffix)
        job = AnonymizationJob(
            id=job_id,
            video_asset_id=asset.id,
            status=JobStatus.QUEUED,
            protection_mode=mode,
        )
        self._store.create(job)
        self._store.update_status(job_id, JobStatus.PROCESSING)
        try:
            anonymize_video(source_path, output_path, summary_path, mode)
            self._store.update_status(job_id, JobStatus.COMPLETED)
        except Exception as exc:
            self._store.update_status(job_id, JobStatus.FAILED, failure_reason=str(exc))
            raise
        return self._store.get(job_id)  # type: ignore[return-value]
