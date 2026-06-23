from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SemanticMode(str, Enum):
    TEXT_ONLY = "text_only"
    OBJECTS_ONLY = "objects_only"
    LAYOUT_ONLY = "layout_only"
    DOCUMENT_ASSIST = "document_assist"
    TASK_GUIDANCE = "task_guidance"
    FULL_SEMANTIC = "full_semantic"


class BoundingBox(BaseModel):
    x: float
    y: float
    w: float
    h: float


class ExtractedText(BaseModel):
    text: str
    confidence: float = Field(ge=0, le=1)
    bbox: Optional[BoundingBox] = None
    redacted: bool = False
    pii_types: List[str] = Field(default_factory=list)


class DetectedObject(BaseModel):
    label: str
    confidence: float = Field(ge=0, le=1)
    bbox: Optional[BoundingBox] = None
    sensitive: bool = False


class LayoutRegion(BaseModel):
    role: str
    bbox: BoundingBox
    text_ref_ids: List[str] = Field(default_factory=list)


class PrivacyAction(BaseModel):
    action: str
    reason: str
    target: str
    policy_id: str


class SemanticPacket(BaseModel):
    packet_id: str
    device_id: str
    session_id: str
    mode: SemanticMode
    user_intent: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    raw_frame_retained: bool = False
    frame_hash: Optional[str] = None
    extracted_texts: List[ExtractedText] = Field(default_factory=list)
    detected_objects: List[DetectedObject] = Field(default_factory=list)
    layout_regions: List[LayoutRegion] = Field(default_factory=list)
    privacy_actions: List[PrivacyAction] = Field(default_factory=list)
    semantic_summary: str = ""
    risk_score: float = Field(default=0.0, ge=0, le=1)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def minimal_payload(self) -> Dict[str, Any]:
        """Return the server-bound payload. Raw pixels are intentionally excluded."""
        return self.model_dump(mode="json", exclude_none=True)
