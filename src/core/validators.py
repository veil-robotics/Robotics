from __future__ import annotations

from pathlib import Path


def validate_input_path(path: Path) -> None:
    if not path.exists():
        raise ValueError(f"Input file not found: {path}")
    if not path.is_file():
        raise ValueError(f"Input path is not a file: {path}")


def validate_output_path(path: Path) -> None:
    if path.exists() and path.is_dir():
        raise ValueError(f"Output path must be a file: {path}")
