from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List
import yaml

from xr_privacy_sdk.models.semantic_packet import DetectedObject, PrivacyAction, SemanticPacket


DEFAULT_SENSITIVE_OBJECTS = {"face", "worker_face", "credit_card", "id_card", "license_plate", "screen", "medical_chart"}


class PolicyEngine:
    def __init__(self, policy: Dict[str, Any] | None = None, policy_path: str | Path | None = None):
        if policy is None and policy_path is not None:
            policy = yaml.safe_load(Path(policy_path).read_text(encoding="utf-8"))
        self.policy = policy or {}
        self.sensitive_objects = set(self.policy.get("sensitive_objects", DEFAULT_SENSITIVE_OBJECTS))
        self.max_risk_for_cloud = float(self.policy.get("max_risk_for_cloud", 0.65))
        self.allow_raw_frame_upload = bool(self.policy.get("allow_raw_frame_upload", False))

    def evaluate_objects(self, objects: Iterable[DetectedObject]) -> tuple[list[DetectedObject], list[PrivacyAction]]:
        sanitized: List[DetectedObject] = []
        actions: List[PrivacyAction] = []
        for obj in objects:
            if obj.label in self.sensitive_objects or obj.sensitive:
                obj = obj.model_copy(update={"sensitive": True})
                actions.append(PrivacyAction(action="suppress_object_region", reason="sensitive_object", target=obj.label, policy_id="object.sensitive.v1"))
            else:
                sanitized.append(obj)
        return sanitized, actions

    def score_risk(self, packet: SemanticPacket) -> float:
        pii_hits = sum(len(t.pii_types) for t in packet.extracted_texts)
        sensitive_actions = sum(1 for a in packet.privacy_actions if "sensitive" in a.reason or "pii" in a.policy_id)
        raw_penalty = 0.5 if packet.raw_frame_retained else 0.0
        risk = min(1.0, 0.1 * pii_hits + 0.15 * sensitive_actions + raw_penalty)
        return round(risk, 3)

    def cloud_allowed(self, packet: SemanticPacket) -> bool:
        if packet.raw_frame_retained and not self.allow_raw_frame_upload:
            return False
        return packet.risk_score <= self.max_risk_for_cloud
