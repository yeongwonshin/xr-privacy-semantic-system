from xr_privacy_sdk.models.semantic_packet import DetectedObject
from xr_privacy_sdk.security.policy_engine import PolicyEngine


def test_sensitive_object_is_suppressed():
    engine = PolicyEngine()
    objects, actions = engine.evaluate_objects([DetectedObject(label="worker_face", confidence=0.9, sensitive=True)])
    assert objects == []
    assert actions[0].action == "suppress_object_region"
