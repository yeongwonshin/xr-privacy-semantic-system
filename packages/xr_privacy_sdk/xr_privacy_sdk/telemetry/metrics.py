from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TransmissionEstimate:
    raw_bytes: int
    semantic_bytes: int

    @property
    def reduction_ratio(self) -> float:
        if self.raw_bytes <= 0:
            return 0.0
        return round(1 - (self.semantic_bytes / self.raw_bytes), 4)


def estimate_payload_savings(raw_frame_bytes: int, semantic_payload: bytes) -> TransmissionEstimate:
    return TransmissionEstimate(raw_bytes=raw_frame_bytes, semantic_bytes=len(semantic_payload))
