from xr_privacy_sdk.pipeline.semantic_runtime import SemanticRuntime


def test_runtime_never_retains_raw_frame():
    runtime = SemanticRuntime(device_id="test-device")
    packet = runtime.build_packet("이 문서를 요약해줘", text_hints=["email me at test@example.com"])
    assert packet.raw_frame_retained is False
    assert packet.extracted_texts[0].redacted is True
    assert "EMAIL_REDACTED" in packet.extracted_texts[0].text
