from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from src.api.app import create_app
from src.core.models import AnonymizationJob, JobStatus, ProtectionMode


def test_api_job_flow(monkeypatch, tmp_path: Path):
    app = create_app()
    client = TestClient(app)

    def fake_run_job(source_path, mode, output_path, summary_path):
        output_path = tmp_path / "job_output.mp4"
        output_path.write_text("out")
        job = AnonymizationJob(
            id=str(uuid4()),
            video_asset_id=str(uuid4()),
            status=JobStatus.COMPLETED,
            protection_mode=ProtectionMode(mode.value),
        )
        app.state.store.create(job)
        return job

    monkeypatch.setattr(app.state.runner, "run_job", fake_run_job)

    create = client.post(
        "/jobs",
        json={"source_path": str(tmp_path / "input.mp4"), "protection_mode": "blur"},
    )
    assert create.status_code == 201
    job_id = create.json()["job_id"]

    status = client.get(f"/jobs/{job_id}")
    assert status.status_code == 200
