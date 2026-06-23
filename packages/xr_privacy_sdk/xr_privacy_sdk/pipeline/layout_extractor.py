from __future__ import annotations

from typing import List
from xr_privacy_sdk.models.semantic_packet import BoundingBox, LayoutRegion


class LayoutExtractor:
    """Simple document-layout baseline for demo and tests."""

    def extract(self, frame: object | None = None) -> List[LayoutRegion]:
        return [
            LayoutRegion(role="title", bbox=BoundingBox(x=0.05, y=0.05, w=0.9, h=0.1)),
            LayoutRegion(role="body", bbox=BoundingBox(x=0.05, y=0.18, w=0.9, h=0.55)),
            LayoutRegion(role="safety_warning", bbox=BoundingBox(x=0.05, y=0.76, w=0.9, h=0.16)),
        ]
