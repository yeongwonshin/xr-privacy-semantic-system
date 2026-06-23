.PHONY: install test demo server edge zip

install:
	pip install -e packages/xr_privacy_sdk -r requirements-dev.txt

test:
	pytest -q

demo:
	python scripts/generate_demo_packet.py

server:
	uvicorn apps.server.main:app --reload --port 8080

edge:
	uvicorn apps.edge_gateway.main:app --reload --port 8070

zip:
	cd .. && zip -r xr_privacy_semantic_ai_platform.zip xr_privacy_semantic_ai_platform
