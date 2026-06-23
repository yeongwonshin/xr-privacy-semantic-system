# Research Notes

## 1. 핵심 연구 방향

최근 AI glasses/XR 연구는 원본 프레임을 계속 클라우드 VLM에 보내는 방식의 한계를 지적한다. 대안은 user intention에 맞춰 텍스트, 문서 레이아웃, 객체 의미 등 task-relevant semantic information만 추출하여 전송하는 것이다.

## 2. 본 프로젝트가 반영한 개념

- Intention-aware semantic communication
- On-device multimodal/VLM interaction
- Privacy-aware XR collaboration
- Edge preprocessing and cloud VLM proxy
- Semantic packet rather than raw-pixel streaming

## 3. 구현 관점

이 레포는 실제 상용화 전에 필요한 baseline 구조를 제공한다.

- 정규식 PII redaction은 production 전 단계 baseline이다.
- OCR/Object/Layout 추출기는 pluggable interface로 두었다.
- Android XR, Unity, OpenXR, Magic Leap, ONNX Runtime adapter를 추가할 수 있다.
- VLM Proxy는 mock 구현이지만 provider adapter 패턴으로 확장 가능하다.

## 4. 논문화/사업화 가능 포인트

- 개인정보 보존율과 업무 정확도의 trade-off 분석
- semantic mode별 네트워크 절감률
- raw frame VLM vs semantic packet VLM 비교
- 산업별 policy profile 자동 생성
- tamper-evident audit log와 XR privacy compliance 결합
