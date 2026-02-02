from __future__ import annotations

from pydantic import BaseModel, Field


class JobCreateRequest(BaseModel):
    source_path: str = Field(..., description="Local path to input video")
    protection_mode: str = Field(..., description="blur or blackout")
    output_path: str | None = Field(None, description="Optional output path")


class JobCreateResponse(BaseModel):
    job_id: str
    status: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    summary: dict | None = None
