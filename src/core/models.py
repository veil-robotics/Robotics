from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ProtectionMode(str, Enum):
    BLUR = "blur"
    BLACKOUT = "blackout"


class TargetType(str, Enum):
    FACE = "face"
    PLATE = "plate"
    SCREEN_TEXT = "screen_text"


@dataclass
class VideoAsset:
    id: str
    source_path: Path
    format: str
    duration: Optional[float] = None
    resolution: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ProtectionRule:
    id: str
    job_id: str
    target_type: TargetType
    mode: ProtectionMode
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnonymizationJob:
    id: str
    video_asset_id: str
    status: JobStatus
    protection_mode: ProtectionMode
    requested_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    failure_reason: Optional[str] = None


@dataclass
class OutputArtifact:
    id: str
    job_id: str
    output_path: Path
    summary_path: Path
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ProcessingSummary:
    id: str
    job_id: str
    protections_applied: List[Dict[str, Any]]
    elapsed_time: float
    warnings: List[str] = field(default_factory=list)
