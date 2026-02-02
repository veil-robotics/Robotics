from __future__ import annotations

from typing import Any

import numpy as np


def _box_blur(frame: np.ndarray, kernel: int = 5) -> np.ndarray:
    if kernel <= 1:
        return frame.copy()
    pad = kernel // 2
    padded = np.pad(frame, ((pad, pad), (pad, pad), (0, 0)), mode="edge")
    blurred = np.zeros_like(frame)
    for y in range(frame.shape[0]):
        for x in range(frame.shape[1]):
            region = padded[y : y + kernel, x : x + kernel]
            blurred[y, x] = region.mean(axis=(0, 1))
    return blurred


def apply_blur(frame: Any) -> Any:
    arr = np.asarray(frame)
    return _box_blur(arr)


def apply_blackout(frame: Any) -> Any:
    arr = np.asarray(frame)
    return np.zeros_like(arr)
