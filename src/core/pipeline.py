from __future__ import annotations

import time
from pathlib import Path
from typing import Iterable, Tuple
from uuid import uuid4

from .models import ProcessingSummary, ProtectionMode
from .obscure import apply_blackout, apply_blur
from .summary import write_summary
from ..io import mp4, rosbag


def _select_adapter(path: Path):
    if path.suffix.lower() == ".mp4":
        return mp4
    if path.suffix.lower() in {".bag", ".rosbag"}:
        return rosbag
    raise ValueError(f"Unsupported input format: {path.suffix}")


def anonymize_frames(
    frames: Iterable[object], mode: ProtectionMode
) -> Iterable[object]:
    for frame in frames:
        if mode == ProtectionMode.BLACKOUT:
            yield apply_blackout(frame)
        else:
            yield apply_blur(frame)


def anonymize_video(
    input_path: Path,
    output_path: Path,
    summary_path: Path,
    mode: ProtectionMode,
) -> ProcessingSummary:
    adapter = _select_adapter(input_path)
    start = time.time()
    info, frames = adapter.read_frames(input_path)
    processed_frames = anonymize_frames(frames, mode)
    adapter.write_frames(output_path, info, processed_frames)
    elapsed = time.time() - start
    summary = ProcessingSummary(
        id=str(uuid4()),
        job_id=str(uuid4()),
        protections_applied=[{"mode": mode.value}],
        elapsed_time=elapsed,
        warnings=[],
    )
    write_summary(summary_path, summary)
    return summary
