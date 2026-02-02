from pathlib import Path

from typer.testing import CliRunner

from src.cli.main import app


runner = CliRunner()


def test_cli_anonymize_runs(monkeypatch, tmp_path: Path):
    input_path = tmp_path / "input.mp4"
    input_path.write_text("dummy")
    output_path = tmp_path / "out.mp4"
    summary_path = tmp_path / "summary.json"

    def fake_anonymize(*_args, **_kwargs):
        output_path.write_text("out")
        summary_path.write_text("summary")

    monkeypatch.setattr("src.cli.anonymize.anonymize_video", fake_anonymize)

    result = runner.invoke(
        app,
        [
            "anonymize",
            str(input_path),
            "--output",
            str(output_path),
            "--summary",
            str(summary_path),
        ],
    )

    assert result.exit_code == 0
    assert output_path.exists()
    assert summary_path.exists()
