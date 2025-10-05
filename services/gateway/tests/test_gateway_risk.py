"""
Test: Proxy /risk/* endpoints to Risk-Engine microservice
"""
import pytest
from fastapi.testclient import TestClient
from services.gateway.gateway import app
import asyncio
from unittest.mock import patch, MagicMock
import httpx

client = TestClient(app)


def make_mock_response(status_code, content, headers):
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.content = content
    mock_resp.headers = headers
    return mock_resp

def async_return(result):
    async def _coro(*args, **kwargs):
        return result
    return _coro

@patch("httpx.AsyncClient.request")
def test_proxy_risk_get(mock_request):
    mock_resp = make_mock_response(200, b'{"risk": "ok"}', {"content-type": "application/json"})
    mock_request.side_effect = async_return(mock_resp)
    resp = client.get("/risk/patient123")
    assert resp.status_code == 200
    assert resp.json()["risk"] == "ok"

@patch("httpx.AsyncClient.request")
def test_proxy_risk_post(mock_request):
    mock_resp = make_mock_response(201, b'{"created": true}', {"content-type": "application/json"})
    mock_request.side_effect = async_return(mock_resp)
    resp = client.post("/risk/config", json={"foo": "bar"})
    assert resp.status_code == 201
    assert resp.json()["created"] is True

@patch("httpx.AsyncClient.request")
def test_proxy_risk_error(mock_request):
    async def raise_exc(*args, **kwargs):
        raise httpx.RequestError("Connection error")
    mock_request.side_effect = raise_exc
    resp = client.get("/risk/patient123")
    assert resp.status_code == 502
    assert "Risk-Engine unavailable" in resp.text
