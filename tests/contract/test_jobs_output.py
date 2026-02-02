from pathlib import Path

from fastapi.testclient import TestClient

from src.api.app import create_app


def test_get_job_output_not_found():
    app = create_app()
    client = TestClient(app)
    response = client.get("/jobs/any/output")
    assert response.status_code == 404


def test_get_job_output_returns_file(tmp_path: Path, monkeypatch):
    app = create_app()
    client = TestClient(app)
    output_path = tmp_path / "job_output.mp4"
    output_path.write_text("data")

    monkeypatch.setattr(
        "src.api.routes.output.Path",
        lambda *_args, **_kwargs: output_path,
    )

    response = client.get("/jobs/any/output")
    assert response.status_code == 200
