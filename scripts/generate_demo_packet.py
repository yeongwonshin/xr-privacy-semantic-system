from pathlib import Path
import json

from xr_privacy_sdk.pipeline.semantic_runtime import SemanticRuntime
from xr_privacy_sdk.security.policy_engine import PolicyEngine
from xr_privacy_sdk.telemetry.metrics import estimate_payload_savings

runtime = SemanticRuntime(device_id="demo-glasses-001", policy_engine=PolicyEngine(policy_path="configs/privacy_policy.yaml"))
packet = runtime.build_packet(
    user_prompt="이 안전 매뉴얼 내용을 요약해줘",
    text_hints=[
        "ACME Safety Manual Section 3",
        "Call supervisor at 010-1234-5678 before opening the panel",
        "Voltage limit: 220V",
    ],
)

out = Path("examples/generated_semantic_packet.json")
out.write_text(json.dumps(packet.minimal_payload(), ensure_ascii=False, indent=2), encoding="utf-8")
semantic_bytes = len(json.dumps(packet.minimal_payload(), ensure_ascii=False).encode("utf-8"))
estimate = estimate_payload_savings(raw_frame_bytes=1920 * 1080 * 3, semantic_payload=b"x" * semantic_bytes)
print(f"wrote: {out}")
print(f"raw_frame_bytes≈{estimate.raw_bytes:,}")
print(f"semantic_payload_bytes≈{estimate.semantic_bytes:,}")
print(f"estimated_reduction≈{estimate.reduction_ratio * 100:.2f}%")
print(json.dumps(packet.minimal_payload(), ensure_ascii=False, indent=2))
