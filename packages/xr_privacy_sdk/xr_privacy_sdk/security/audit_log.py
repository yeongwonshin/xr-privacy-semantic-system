from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


class TamperEvidentAuditLog:
    """Append-only audit log with hash chaining.

    This is not a replacement for WORM storage or SIEM, but it gives the SDK a portable
    integrity primitive that can be forwarded to enterprise logging systems.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._last_hash = self._load_last_hash()

    def _load_last_hash(self) -> str:
        if not self.path.exists():
            return "GENESIS"
        lines = [line for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not lines:
            return "GENESIS"
        try:
            return json.loads(lines[-1])["entry_hash"]
        except Exception:
            return "CORRUPTED"

    def append(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "prev_hash": self._last_hash,
            "payload": payload,
        }
        canonical = json.dumps(record, sort_keys=True, ensure_ascii=False).encode("utf-8")
        entry_hash = hashlib.sha256(canonical).hexdigest()
        record["entry_hash"] = entry_hash
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        self._last_hash = entry_hash
        return record
