from __future__ import annotations

import hashlib
import uuid
from typing import Iterable, Optional

from xr_privacy_sdk.models.semantic_packet import SemanticMode, SemanticPacket
from xr_privacy_sdk.pipeline.intent_classifier import IntentClassifier
from xr_privacy_sdk.pipeline.layout_extractor import LayoutExtractor
from xr_privacy_sdk.pipeline.object_extractor import ObjectExtractor
from xr_privacy_sdk.pipeline.ocr_extractor import OCRExtractor
from xr_privacy_sdk.security.policy_engine import PolicyEngine
from xr_privacy_sdk.security.redactor import SensitiveDataRedactor


class SemanticRuntime:
    """On-device semantic pipeline.

    The runtime intentionally returns a semantic packet and never returns raw image bytes.
    """

    def __init__(
        self,
        device_id: str,
        policy_engine: PolicyEngine | None = None,
        ocr: OCRExtractor | None = None,
        objects: ObjectExtractor | None = None,
        layout: LayoutExtractor | None = None,
        classifier: IntentClassifier | None = None,
    ):
        self.device_id = device_id
        self.policy_engine = policy_engine or PolicyEngine()
        self.ocr = ocr or OCRExtractor()
        self.objects = objects or ObjectExtractor()
        self.layout = layout or LayoutExtractor()
        self.classifier = classifier or IntentClassifier()
        self.redactor = SensitiveDataRedactor()

    def build_packet(
        self,
        user_prompt: str,
        frame: object | None = None,
        text_hints: Iterable[str] | None = None,
        session_id: Optional[str] = None,
    ) -> SemanticPacket:
        mode = self.classifier.classify(user_prompt)
        packet_id = str(uuid.uuid4())
        session_id = session_id or str(uuid.uuid4())
        frame_hash = self._safe_frame_hash(frame)

        extracted_texts = []
        detected_objects = []
        layout_regions = []
        privacy_actions = []

        if mode in {SemanticMode.TEXT_ONLY, SemanticMode.DOCUMENT_ASSIST, SemanticMode.FULL_SEMANTIC, SemanticMode.LAYOUT_ONLY}:
            extracted_texts = self.ocr.extract(frame=frame, hints=text_hints)
            extracted_texts, redaction_actions = self.redactor.redact_texts(extracted_texts)
            privacy_actions.extend(redaction_actions)

        if mode in {SemanticMode.OBJECTS_ONLY, SemanticMode.TASK_GUIDANCE, SemanticMode.FULL_SEMANTIC}:
            detected_objects = self.objects.detect(frame=frame)
            detected_objects, object_actions = self.policy_engine.evaluate_objects(detected_objects)
            privacy_actions.extend(object_actions)

        if mode in {SemanticMode.LAYOUT_ONLY, SemanticMode.DOCUMENT_ASSIST, SemanticMode.FULL_SEMANTIC}:
            layout_regions = self.layout.extract(frame=frame)

        semantic_summary = self._summarize(mode, extracted_texts, detected_objects, layout_regions)

        packet = SemanticPacket(
            packet_id=packet_id,
            device_id=self.device_id,
            session_id=session_id,
            mode=mode,
            user_intent=user_prompt,
            raw_frame_retained=False,
            frame_hash=frame_hash,
            extracted_texts=extracted_texts,
            detected_objects=detected_objects,
            layout_regions=layout_regions,
            privacy_actions=privacy_actions,
            semantic_summary=semantic_summary,
            metadata={"sdk_version": "0.1.0", "pipeline": "mockable-edge-runtime"},
        )
        packet.risk_score = self.policy_engine.score_risk(packet)
        return packet

    @staticmethod
    def _safe_frame_hash(frame: object | None) -> str | None:
        if frame is None:
            return None
        if isinstance(frame, bytes):
            return hashlib.sha256(frame).hexdigest()
        return hashlib.sha256(repr(type(frame)).encode()).hexdigest()

    @staticmethod
    def _summarize(mode, texts, objects, layout_regions) -> str:
        parts = [f"mode={mode.value}"]
        if texts:
            parts.append("texts=" + "; ".join(t.text for t in texts[:3]))
        if objects:
            parts.append("objects=" + ", ".join(o.label for o in objects[:5]))
        if layout_regions:
            parts.append("layout=" + ", ".join(r.role for r in layout_regions[:5]))
        return " | ".join(parts)
