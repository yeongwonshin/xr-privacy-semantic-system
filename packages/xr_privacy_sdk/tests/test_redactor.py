from xr_privacy_sdk.models.semantic_packet import ExtractedText
from xr_privacy_sdk.security.redactor import SensitiveDataRedactor


def test_redacts_korean_phone_number():
    redactor = SensitiveDataRedactor()
    texts, actions = redactor.redact_texts([ExtractedText(text="전화 010-1234-5678", confidence=0.9)])
    assert "PHONE_KR_REDACTED" in texts[0].text
    assert texts[0].redacted is True
    assert actions[0].action == "redact_text"
