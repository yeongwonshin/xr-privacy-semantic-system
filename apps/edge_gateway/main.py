from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from xr_privacy_sdk.pipeline.semantic_runtime import SemanticRuntime
from xr_privacy_sdk.security.policy_engine import PolicyEngine

app = FastAPI(title="XR Edge Semantic Gateway", version="0.1.0")
runtime = SemanticRuntime(device_id="dev-glasses-001", policy_engine=PolicyEngine())


class EdgeAnalyzeRequest(BaseModel):
    prompt: str
    text_hints: list[str] | None = None
    session_id: str | None = None


@app.get("/health")
def health():
    return {"ok": True, "service": "edge-gateway", "raw_frame_upload_default": False}


@app.post("/v1/edge/analyze")
def analyze(req: EdgeAnalyzeRequest):
    packet = runtime.build_packet(user_prompt=req.prompt, text_hints=req.text_hints, session_id=req.session_id)
    return packet.minimal_payload()
