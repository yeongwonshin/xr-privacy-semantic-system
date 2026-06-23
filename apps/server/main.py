from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from xr_privacy_sdk.models.semantic_packet import SemanticPacket
from xr_privacy_sdk.security.audit_log import TamperEvidentAuditLog
from xr_privacy_sdk.security.policy_engine import PolicyEngine

app = FastAPI(title="XR Privacy Semantic Server", version="0.1.0")
audit = TamperEvidentAuditLog(Path(".local/server_audit/audit.log"))
policy = PolicyEngine()


class VLMResponse(BaseModel):
    answer: str
    blocked: bool = False
    risk_score: float
    metadata: dict = {}


@app.get("/health")
def health():
    return {"ok": True, "service": "xr-privacy-semantic-server", "version": "0.1.0"}


@app.post("/v1/vlm/query", response_model=VLMResponse)
def query_vlm(packet: SemanticPacket):
    packet.risk_score = policy.score_risk(packet)
    audit.append("server_packet_received", packet.minimal_payload())

    if not policy.cloud_allowed(packet):
        audit.append("server_packet_blocked", {"packet_id": packet.packet_id, "risk_score": packet.risk_score})
        return VLMResponse(answer="정책상 서버 VLM 질의가 차단되었습니다. Edge에서 더 많은 정보를 제거한 뒤 재시도하세요.", blocked=True, risk_score=packet.risk_score)

    answer = mock_vlm_reasoning(packet)
    audit.append("server_vlm_mock_completed", {"packet_id": packet.packet_id, "answer_len": len(answer)})
    return VLMResponse(answer=answer, risk_score=packet.risk_score, metadata={"provider": "mock", "raw_pixels_seen": False})


@app.post("/v1/policy/evaluate")
def evaluate_policy(packet: SemanticPacket):
    packet.risk_score = policy.score_risk(packet)
    return {"packet_id": packet.packet_id, "risk_score": packet.risk_score, "cloud_allowed": policy.cloud_allowed(packet), "actions": [a.model_dump() for a in packet.privacy_actions]}


@app.get("/v1/audit/tail")
def audit_tail(limit: int = 20):
    path = Path(".local/server_audit/audit.log")
    if not path.exists():
        return {"items": []}
    lines = path.read_text(encoding="utf-8").splitlines()[-limit:]
    return {"items": lines}


def mock_vlm_reasoning(packet: SemanticPacket) -> str:
    if packet.extracted_texts:
        text = " / ".join(t.text for t in packet.extracted_texts)
        return f"원본 이미지 없이 추출된 텍스트 기준으로 답변합니다: {text}. 민감정보는 이미 제거되었습니다."
    if packet.detected_objects:
        objects = ", ".join(o.label for o in packet.detected_objects)
        return f"객체 의미 정보만 기준으로 판단했습니다. 감지된 비민감 객체: {objects}."
    return f"전송된 semantic summary 기준 응답: {packet.semantic_summary}"
