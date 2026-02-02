from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from src.api.app import create_app
from src.core.models import AnonymizationJob, JobStatus, ProtectionMode


def test_create_job_returns_job_id(monkeypatch):
    app = create_app()
    client = TestClient(app)

    def fake_run_job(source_path, mode, output_path, summary_path):
        job = AnonymizationJob(
            id=str(uuid4()),
            video_asset_id=str(uuid4()),
            status=JobStatus.COMPLETED,
            protection_mode=ProtectionMode(mode.value),
        )
        app.state.store.create(job)
        return job

    monkeypatch.setattr(app.state.runner, "run_job", fake_run_job)

    response = client.post(
        "/jobs",
        json={"source_path": str(Path("input.mp4")), "protection_mode": "blur"},
    )

    assert response.status_code == 201
    assert response.json()["status"] in {"completed", "queued", "processing"}
