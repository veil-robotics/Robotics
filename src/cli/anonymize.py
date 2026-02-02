from __future__ import annotations

from pathlib import Path

import typer

from ..core.config import load_config
from ..core.modes import parse_mode
from ..core.pipeline import anonymize_video
from ..core.validators import validate_input_path, validate_output_path

app = typer.Typer(add_completion=False)


@app.command()
def run(
    input_path: Path = typer.Argument(..., help="Path to input video"),
    output_path: Path = typer.Option(None, "--output", help="Output video path"),
    summary_path: Path = typer.Option(
        None, "--summary", help="Processing summary output path"
    ),
    mode: str = typer.Option("blur", "--mode", help="blur or blackout"),
) -> None:
    config = load_config()
    output = output_path or config.output_dir / f"{input_path.stem}_sanitized.mp4"
    summary = summary_path or config.summary_dir / f"{input_path.stem}_summary.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    validate_input_path(input_path)
    validate_output_path(output)
    anonymize_video(input_path, output, summary, parse_mode(mode))
    typer.echo(f"Sanitized video written to {output}")
    typer.echo(f"Summary written to {summary}")
