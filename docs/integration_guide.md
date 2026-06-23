# Integration Guide

## 1. XR 앱 연동 방식

### Python/Edge Gateway 방식
XR 디바이스 또는 companion device에서 Edge Gateway를 띄우고 XR 앱이 로컬 HTTP로 호출한다.

### Native SDK 방식
향후 Android XR/Unity/OpenXR용 wrapper를 제공한다.

## 2. Adapter 구현 예시

```python
class MyOCRExtractor:
    def extract(self, frame, hints=None):
        # Call ML Kit / PaddleOCR / ONNX Runtime here
        return [ExtractedText(text="...", confidence=0.91)]
```

## 3. 운영환경 체크리스트

- raw frame upload가 꺼져 있는지 확인
- policy version을 audit에 남기는지 확인
- VLM provider에 semantic packet만 전달되는지 확인
- API key/mTLS 적용
- SIEM/로그 저장소 연동
- 민감정보 샘플셋 red-team 테스트
