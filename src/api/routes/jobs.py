from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException, Request

from ...core.modes import parse_mode
from ...core.models import JobStatus
from ..schemas import JobCreateRequest, JobCreateResponse, JobStatusResponse

router = APIRouter()


@router.post("/jobs", response_model=JobCreateResponse, status_code=201)
def create_job(payload: JobCreateRequest, request: Request) -> JobCreateResponse:
    runner = request.app.state.runner
    output_path = Path(payload.output_path) if payload.output_path else Path("outputs") / "job_output.mp4"
    summary_path = Path("summaries") / "job_summary.json"
    try:
        job = runner.run_job(Path(payload.source_path), parse_mode(payload.protection_mode), output_path, summary_path)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return JobCreateResponse(job_id=job.id, status=job.status.value)


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
def get_job(job_id: str, request: Request) -> JobStatusResponse:
    store = request.app.state.store
    job = store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    summary = None
    if job.status == JobStatus.COMPLETED:
        summary = {"job_id": job.id}
    return JobStatusResponse(job_id=job.id, status=job.status.value, summary=summary)
