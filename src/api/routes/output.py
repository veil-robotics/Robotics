from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/jobs/{job_id}/output")
def get_output(job_id: str) -> FileResponse:
    output_path = Path("outputs") / "job_output.mp4"
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="Output not available")
    return FileResponse(str(output_path), media_type="video/mp4")
