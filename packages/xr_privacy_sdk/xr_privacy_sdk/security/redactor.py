from __future__ import annotations

import re
from typing import Iterable, List, Tuple
from xr_privacy_sdk.models.semantic_packet import ExtractedText, PrivacyAction


class SensitiveDataRedactor:
    """Redacts common PII before semantic packets leave the device."""

    PATTERNS: List[Tuple[str, re.Pattern]] = [
        ("email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
        ("phone_kr", re.compile(r"01[016789]-?\d{3,4}-?\d{4}")),
        ("credit_card", re.compile(r"(?:\d[ -]*?){13,16}")),
        ("resident_id_kr_like", re.compile(r"\d{6}-[1-4]\d{6}")),
    ]

    def redact_texts(self, texts: Iterable[ExtractedText], policy_id: str = "pii.regex.v1") -> tuple[list[ExtractedText], list[PrivacyAction]]:
        redacted: list[ExtractedText] = []
        actions: list[PrivacyAction] = []
        for item in texts:
            new_text = item.text
            pii_types: list[str] = []
            for pii_type, pattern in self.PATTERNS:
                if pattern.search(new_text):
                    pii_types.append(pii_type)
                    new_text = pattern.sub(f"[{pii_type.upper()}_REDACTED]", new_text)
            if pii_types:
                item = item.model_copy(update={"text": new_text, "redacted": True, "pii_types": pii_types})
                actions.append(PrivacyAction(action="redact_text", reason=",".join(pii_types), target=item.text, policy_id=policy_id))
            redacted.append(item)
        return redacted, actions
