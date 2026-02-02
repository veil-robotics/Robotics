import numpy as np

from src.core.models import ProtectionMode
from src.core.pipeline import anonymize_frames


def test_anonymize_frames_blur_changes_pixels():
    frame = np.random.randint(0, 255, (5, 5, 3), dtype=np.uint8)
    blurred = list(anonymize_frames([frame], ProtectionMode.BLUR))[0]
    assert blurred.shape == frame.shape
    assert not np.array_equal(blurred, frame)


def test_anonymize_frames_blackout_zeroes():
    frame = np.random.randint(0, 255, (5, 5, 3), dtype=np.uint8)
    blacked = list(anonymize_frames([frame], ProtectionMode.BLACKOUT))[0]
    assert np.count_nonzero(blacked) == 0
