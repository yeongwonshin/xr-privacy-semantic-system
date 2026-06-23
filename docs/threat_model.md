# Threat Model

## 1. 보호 대상

- 주변인의 얼굴과 음성 맥락
- 신분증/카드/전화번호/이메일/주소
- 환자·학생·근로자 식별정보
- 사내 기밀 화면, 설비 배치, 문서
- 사용자의 시선/행동 패턴 로그

## 2. 공격자 모델

| 공격자 | 위험 |
|---|---|
| Cloud VLM Provider | 원본 프레임 또는 민감 맥락 수신 |
| 악성 XR 앱 | SDK 우회 후 raw frame 전송 |
| 내부자 | 감사 로그 삭제/변조 |
| 네트워크 공격자 | semantic packet 탈취 |
| 부정확한 모델 | 민감정보 탐지 실패 |

## 3. 방어 전략

### Data Minimization
원본 프레임을 서버에 보내지 않고 semantic packet만 전송한다.

### Policy Gate
cloud 전송 전 Edge와 Server에서 이중 정책 검사를 수행한다.

### PII Redaction
정규식 기반 baseline에서 시작하여 OCR+NER+vision sensitive object detector로 확장한다.

### Sensitive Object Suppression
얼굴, 카드, ID, 의료 차트, 타인 화면 등은 객체 단위로 suppress한다.

### Audit Integrity
해시 체인 기반 로그를 남겨 삭제/변조 징후를 탐지한다.

## 4. 잔여 리스크

- OCR이 민감 텍스트를 놓칠 수 있다.
- 객체 탐지가 얼굴/카드 일부를 놓칠 수 있다.
- semantic packet 자체가 문맥상 민감할 수 있다.
- 사용자가 악의적으로 프롬프트를 넣어 우회할 수 있다.

## 5. 완화 로드맵

- 온디바이스 small VLM으로 민감 문맥 판정
- differential privacy 기반 통계 로그
- secure enclave/key attestation
- enterprise MDM 정책 연동
- red-team prompt test suite
