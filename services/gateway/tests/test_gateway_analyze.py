"""
Test: End-to-end pipeline flow for /analyze/prescription
"""


import pytest
from fastapi.testclient import TestClient
from services.gateway.gateway import app

from unittest.mock import AsyncMock

client = TestClient(app)

class DummyResp:
    def __init__(self, data):
        self.status_code = 200
        self._data = data
    def json(self):
        return self._data



from services.gateway.routers import analyze as analyze_router

class MockHttpClient:
    async def post(self, url, *args, **kwargs):
        if "ocr" in url:
            return DummyResp({"text": "Take Aspirin 100mg OD 5d"})
        elif "ner" in url:
            return DummyResp({"drugs": [{"drug_id": "drugA", "name": "Aspirin", "dose": "100mg", "freq": "OD", "duration": "5d"}]})
        elif "risk" in url:
            return DummyResp({"risk_score": 0.8, "level": "HIGH"})
        else:
            return DummyResp({})
    async def get(self, url, *args, **kwargs):
        return DummyResp({"features": [0.1, 0.2]})

async def override_http_client():
    yield MockHttpClient()

def test_analyze_prescription():
    # Patch FastAPI dependency for http_client
    app.dependency_overrides[analyze_router.default_http_client] = override_http_client
    with open("/dev/null", "rb") as f:
        response = client.post("/analyze/prescription", data={"patient_id": "patient123"}, files={"file": ("rx.png", f, "image/png")})
    assert response.status_code == 200
    data = response.json()
    assert data["ocr_text"]
    assert data["drugs"]
    assert data["features"]
    assert data["risk"]["level"] == "HIGH"
    # Clean up override
    app.dependency_overrides = {}
