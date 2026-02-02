from uuid import uuid4

from fastapi.testclient import TestClient

from src.api.app import create_app
from src.core.models import AnonymizationJob, JobStatus, ProtectionMode


def test_get_job_status(monkeypatch):
    app = create_app()
    client = TestClient(app)
    job = AnonymizationJob(
        id=str(uuid4()),
        video_asset_id=str(uuid4()),
        status=JobStatus.COMPLETED,
        protection_mode=ProtectionMode.BLUR,
    )
    app.state.store.create(job)

    response = client.get(f"/jobs/{job.id}")

    assert response.status_code == 200
    assert response.json()["status"] == "completed"
