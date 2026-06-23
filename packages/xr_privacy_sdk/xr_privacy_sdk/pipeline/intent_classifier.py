from __future__ import annotations

from xr_privacy_sdk.models.semantic_packet import SemanticMode


class IntentClassifier:
    """Rule-based baseline. Replace with on-device tiny classifier in production."""

    DOCUMENT_KEYWORDS = {"read", "translate", "summarize", "document", "menu", "receipt", "manual", "문서", "번역", "요약", "영수증", "매뉴얼"}
    OBJECT_KEYWORDS = {"what is", "identify", "object", "part", "tool", "hazard", "객체", "부품", "위험", "도구"}
    LAYOUT_KEYWORDS = {"layout", "table", "form", "slide", "chart", "표", "양식", "슬라이드", "차트"}

    def classify(self, prompt: str) -> SemanticMode:
        p = prompt.lower()
        if any(k in p for k in self.LAYOUT_KEYWORDS):
            return SemanticMode.LAYOUT_ONLY
        if any(k in p for k in self.DOCUMENT_KEYWORDS):
            return SemanticMode.DOCUMENT_ASSIST
        if any(k in p for k in self.OBJECT_KEYWORDS):
            return SemanticMode.OBJECTS_ONLY
        return SemanticMode.FULL_SEMANTIC
