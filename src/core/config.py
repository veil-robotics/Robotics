from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    output_dir: Path
    summary_dir: Path
    log_level: str


def load_config() -> AppConfig:
    base_dir = Path(os.getenv("ANONYMIZE_BASE_DIR", Path.cwd()))
    output_dir = Path(os.getenv("ANONYMIZE_OUTPUT_DIR", base_dir / "outputs"))
    summary_dir = Path(os.getenv("ANONYMIZE_SUMMARY_DIR", base_dir / "summaries"))
    log_level = os.getenv("ANONYMIZE_LOG_LEVEL", "INFO")
    return AppConfig(output_dir=output_dir, summary_dir=summary_dir, log_level=log_level)
