# Product Spec: XR Privacy Semantic AI Platform

## 1. 문제 정의

스마트글래스와 XR 헤드셋은 사용자의 1인칭 시야를 계속 수집할 수 있다. 이 데이터에는 문서, 얼굴, 신분증, 결제정보, 의료정보, 학생 정보, 사내 기밀 화면 등이 함께 포착된다. 기존 클라우드 VLM 방식은 전체 프레임을 서버에 전송하기 때문에 개인정보·보안·대역폭·전력 문제가 동시에 발생한다.

## 2. 제품 비전

원본 영상이 아니라 **작업 의도에 필요한 최소 semantic representation**만 전송하는 기업용 XR AI 보안 SDK를 제공한다.

## 3. 목표 고객

- XR 스마트글래스 제조사
- 산업 안전/정비 솔루션 기업
- 의료 교육 XR 기업
- 공공기관/군/보안구역용 XR 솔루션
- 교육 XR 플랫폼

## 4. 핵심 기능

### 4.1 Semantic Extraction SDK
- OCR 텍스트 추출
- 객체 탐지
- 문서 레이아웃 추출
- 작업 의도별 semantic mode 선택
- raw frame server upload 차단

### 4.2 Privacy Guard
- 얼굴/신분증/카드/전화번호/이메일 탐지
- 정책 기반 masking/suppression/blocking
- 지역·조직·업무별 policy profile

### 4.3 VLM Proxy
- 서버 VLM은 semantic packet만 수신
- provider adapter 구조: OpenAI, Gemini, Claude, 온프레미스 모델 등으로 교체 가능
- 민감도 높은 packet은 cloud query 차단

### 4.4 Audit & Compliance
- 전송 전후 이벤트 감사 로그
- 해시 체인 기반 tamper-evident log
- DPO/보안팀용 리포트
- raw pixel non-retention 증적

## 5. 차별화

| 기존 XR AI 앱 | 본 시스템 |
|---|---|
| 카메라 프레임을 VLM 서버로 업로드 | 원본 프레임 제외, 의미 정보만 전송 |
| 앱별 임시 masking | SDK 단위 일관 정책 엔진 |
| 기능 중심 | 개인정보·보안·감사 중심 |
| VLM API 호출 로그만 존재 | Edge extraction부터 VLM 응답까지 end-to-end audit |
| 데모앱 | 기업용 SDK/온프레미스/정책 콘솔 |

## 6. KPI

- Raw frame upload rate: 0% 기본값
- Semantic payload size reduction: 시나리오별 50%+ 목표
- PII redaction precision/recall
- Cloud query block false positive rate
- Edge latency p95
- Audit completeness
- Battery/network usage reduction

## 7. 유료화

- 디바이스당 SDK 라이선스
- 월간 semantic packet 처리량 과금
- 온프레미스 VLM Proxy 구축비
- 산업별 policy/profile template 판매
- 감사 리포트 SaaS
