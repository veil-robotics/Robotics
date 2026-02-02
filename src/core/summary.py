from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Dict

from .models import ProcessingSummary


def write_summary(path: Path, summary: ProcessingSummary) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: Dict[str, object] = asdict(summary)
    path.write_text(json.dumps(payload, indent=2, default=str))
