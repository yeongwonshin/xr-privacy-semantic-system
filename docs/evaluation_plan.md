# Evaluation Plan

## 1. Privacy Evaluation

- PII redaction precision/recall
- sensitive object suppression rate
- raw frame upload rate
- policy bypass success rate
- prompt injection resistance

## 2. Utility Evaluation

- 원본 이미지 VLM 답변 대비 semantic packet 답변 정확도
- task completion rate
- document QA accuracy
- object guidance accuracy
- layout understanding score

## 3. Efficiency Evaluation

- raw frame bytes vs semantic packet bytes
- edge latency p50/p95/p99
- server latency p95
- battery usage estimate
- network usage estimate

## 4. Enterprise Readiness

- audit log completeness
- policy versioning
- tenant isolation
- SDK integration time
- on-prem deployment reproducibility

## 5. Benchmark Scenarios

| Scenario | Input | Expected Semantic Mode | Main Metric |
|---|---|---|---|
| Manual Summarization | 산업 매뉴얼 | document_assist | QA accuracy, PII recall |
| Hazard Guidance | 장비/경고표지 | task_guidance | object precision, latency |
| Medical Training | 차트/기기 | layout_only/document_assist | PHI suppression |
| Classroom XR | 판서/문제지 | text_only/layout_only | student privacy recall |
