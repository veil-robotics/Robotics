from __future__ import annotations

from pathlib import Path
from typing import Iterable, Tuple


class RosbagNotSupported(RuntimeError):
    pass


def read_frames(path: Path) -> Tuple[object, Iterable[object]]:
    raise RosbagNotSupported(
        "ROS bag support is not yet implemented. Provide MP4 input for now."
    )


def write_frames(path: Path, info: object, frames: Iterable[object]) -> None:
    raise RosbagNotSupported(
        "ROS bag output is not yet implemented. Provide MP4 output for now."
    )
