# API Contract

## POST /v1/edge/analyze

Edge Runtime에서 prompt를 받아 semantic packet을 생성한다.

### Request

```json
{
  "prompt": "이 매뉴얼 내용을 요약해줘",
  "text_hints": ["Call 010-1234-5678"],
  "session_id": "session-001"
}
```

### Response

```json
{
  "packet_id": "...",
  "mode": "document_assist",
  "raw_frame_retained": false,
  "extracted_texts": [],
  "privacy_actions": [],
  "risk_score": 0.1
}
```

## POST /v1/vlm/query

서버 VLM Proxy가 semantic packet을 받아 답변을 생성한다.

### Security

- Authorization: Bearer token
- mTLS 권장
- packet-level risk score 검증

## POST /v1/policy/evaluate

packet이 cloud VLM으로 갈 수 있는지 평가한다.

## GET /v1/audit/tail

최근 감사 로그를 조회한다. 운영환경에서는 관리자 인증과 pagination을 추가해야 한다.
