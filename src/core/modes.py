from __future__ import annotations

from .models import ProtectionMode


def parse_mode(value: str) -> ProtectionMode:
    try:
        return ProtectionMode(value)
    except ValueError as exc:
        raise ValueError(f"Unsupported protection mode: {value}") from exc
