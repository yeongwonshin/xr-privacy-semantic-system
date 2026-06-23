from __future__ import annotations

from pathlib import Path
from xr_privacy_sdk.pipeline.semantic_runtime import SemanticRuntime
from xr_privacy_sdk.security.audit_log import TamperEvidentAuditLog
from xr_privacy_sdk.security.policy_engine import PolicyEngine
from xr_privacy_sdk.transport.secure_client import SecureSemanticClient


class XRPrivacyClient:
    """High-level SDK facade used by XR applications."""

    def __init__(self, device_id: str, server_url: str, api_key: str | None = None, policy_path: str | None = None, audit_path: str = ".local/audit/audit.log"):
        self.policy = PolicyEngine(policy_path=policy_path) if policy_path else PolicyEngine()
        self.runtime = SemanticRuntime(device_id=device_id, policy_engine=self.policy)
        self.transport = SecureSemanticClient(server_url, api_key=api_key)
        self.audit = TamperEvidentAuditLog(Path(audit_path))

    async def ask(self, user_prompt: str, frame: object | None = None) -> dict:
        packet = self.runtime.build_packet(user_prompt=user_prompt, frame=frame)
        self.audit.append("semantic_packet_created", packet.minimal_payload())
        if not self.policy.cloud_allowed(packet):
            self.audit.append("cloud_blocked", {"packet_id": packet.packet_id, "risk_score": packet.risk_score})
            return {"blocked": True, "reason": "policy_risk_threshold", "packet": packet.minimal_payload()}
        response = await self.transport.query_vlm(packet)
        self.audit.append("vlm_response_received", {"packet_id": packet.packet_id, "response_meta": response.get("metadata", {})})
        return response
