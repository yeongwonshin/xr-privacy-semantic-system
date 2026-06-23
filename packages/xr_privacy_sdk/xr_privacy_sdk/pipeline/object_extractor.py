from __future__ import annotations

from typing import Iterable, List, Tuple
from xr_privacy_sdk.models.semantic_packet import DetectedObject, BoundingBox


class ObjectExtractor:
    """Pluggable object detector interface.

    Production adapters can wrap YOLOv8/YOLO-NAS/MediaPipe/ONNX Runtime or device-vendor APIs.
    """

    def detect(self, frame: object | None = None, hints: Iterable[Tuple[str, float]] | None = None) -> List[DetectedObject]:
        if hints is None:
            hints = [("control_panel", 0.91), ("worker_face", 0.88), ("credit_card", 0.79), ("warning_label", 0.96)]
        objects: List[DetectedObject] = []
        x = 0.04
        for label, conf in hints:
            objects.append(
                DetectedObject(
                    label=label,
                    confidence=conf,
                    bbox=BoundingBox(x=x, y=0.2, w=0.18, h=0.16),
                    sensitive=label in {"worker_face", "face", "credit_card", "license_plate", "id_card"},
                )
            )
            x += 0.21
        return objects
