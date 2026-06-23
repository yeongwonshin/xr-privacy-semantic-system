"""Minimal audit dashboard.

Run:
    streamlit run apps/dashboard/audit_dashboard.py
"""
from pathlib import Path
import json
import pandas as pd
import streamlit as st

st.set_page_config(page_title="XR Privacy Audit", layout="wide")
st.title("XR Privacy Semantic AI - Audit Dashboard")
path = Path(".local/server_audit/audit.log")
if not path.exists():
    st.info("아직 감사 로그가 없습니다. 서버 API를 먼저 호출하세요.")
    st.stop()
rows = []
for line in path.read_text(encoding="utf-8").splitlines():
    try:
        rows.append(json.loads(line))
    except Exception:
        rows.append({"event_type": "parse_error", "raw": line})

df = pd.DataFrame(rows)
st.metric("Audit Events", len(df))
st.dataframe(df, use_container_width=True)
