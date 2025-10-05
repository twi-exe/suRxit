"""
Test: /alerts endpoints (list, get)
"""
from fastapi.testclient import TestClient
from services.gateway.gateway import app

client = TestClient(app)

def test_list_alerts():
    resp = client.get("/alerts/")
    assert resp.status_code == 200
    alerts = resp.json()
    assert isinstance(alerts, list)
    assert any(a["id"] == "a1" for a in alerts)

def test_list_alerts_filter_patient():
    resp = client.get("/alerts/?patient_id=p1")
    assert resp.status_code == 200
    alerts = resp.json()
    assert all(a["patient_id"] == "p1" for a in alerts)
    assert len(alerts) > 0

def test_list_alerts_unread_only():
    resp = client.get("/alerts/?unread_only=true")
    assert resp.status_code == 200
    alerts = resp.json()
    assert all(a["status"] == "unread" for a in alerts)

def test_get_alert():
    resp = client.get("/alerts/a2")
    assert resp.status_code == 200
    alert = resp.json()
    assert alert["id"] == "a2"
    assert alert["type"] == "ADR"

def test_get_alert_not_found():
    resp = client.get("/alerts/doesnotexist")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Alert not found"
