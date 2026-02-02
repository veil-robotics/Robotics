import pytest

from src.core.modes import parse_mode
from src.core.models import ProtectionMode


def test_parse_mode_accepts_blur():
    assert parse_mode("blur") == ProtectionMode.BLUR


def test_parse_mode_invalid():
    with pytest.raises(ValueError):
        parse_mode("invalid")
