from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Tuple


@dataclass
class VideoInfo:
    fps: float
    size: Tuple[int, int]
    frame_count: int


def _require_cv2() -> "object":
    try:
        import cv2  # type: ignore
    except Exception as exc:  # pragma: no cover - runtime dependency
        raise RuntimeError("OpenCV is required for MP4 processing") from exc
    return cv2


def read_frames(path: Path) -> Tuple[VideoInfo, Iterable[object]]:
    cv2 = _require_cv2()
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError(f"Unable to open video: {path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def _iter() -> Iterable[object]:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            yield frame
        cap.release()

    return VideoInfo(fps=fps, size=(width, height), frame_count=frame_count), _iter()


def write_frames(path: Path, info: VideoInfo, frames: Iterable[object]) -> None:
    cv2 = _require_cv2()
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(path), fourcc, info.fps, info.size)
    if not writer.isOpened():
        raise ValueError(f"Unable to write video: {path}")
    for frame in frames:
        writer.write(frame)
    writer.release()
