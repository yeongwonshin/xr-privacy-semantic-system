from __future__ import annotations

from typing import Iterable, List
from xr_privacy_sdk.models.semantic_packet import ExtractedText, BoundingBox


class OCRExtractor:
    """Pluggable OCR interface.

    Production adapters can wrap ML Kit, EasyOCR, PaddleOCR, Tesseract, or Android XR native APIs.
    The default implementation accepts pre-tokenized text for deterministic tests and demos.
    """

    def extract(self, frame: object | None = None, hints: Iterable[str] | None = None) -> List[ExtractedText]:
        if hints is None:
            hints = [
                "ACME Safety Manual Section 3",
                "Call supervisor at 010-1234-5678 before opening the panel",
                "Voltage limit: 220V",
            ]
        results: List[ExtractedText] = []
        y = 0.05
        for text in hints:
            results.append(
                ExtractedText(
                    text=text,
                    confidence=0.93,
                    bbox=BoundingBox(x=0.05, y=y, w=0.85, h=0.08),
                )
            )
            y += 0.1
        return results
