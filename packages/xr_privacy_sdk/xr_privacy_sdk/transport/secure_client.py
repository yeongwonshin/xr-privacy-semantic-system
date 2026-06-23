from __future__ import annotations

import httpx
from xr_privacy_sdk.models.semantic_packet import SemanticPacket


class SecureSemanticClient:
    def __init__(self, base_url: str, api_key: str | None = None, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    async def query_vlm(self, packet: SemanticPacket) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(f"{self.base_url}/v1/vlm/query", json=packet.minimal_payload(), headers=headers)
            response.raise_for_status()
            return response.json()
