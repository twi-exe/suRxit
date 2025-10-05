"""
Test: /patient endpoints (CRUD, prescriptions, allergies)
"""
from fastapi.testclient import TestClient
from services.gateway.gateway import app

client = TestClient(app)

def test_list_patients():
    resp = client.get("/patient/")
    assert resp.status_code == 200
    patients = resp.json()
    assert any(p["id"] == "p1" for p in patients)

def test_get_patient():
    resp = client.get("/patient/p1")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Alice"

def test_create_patient():
    new_patient = {"id": "p3", "name": "Carol", "age": 30, "allergies": [], "prescriptions": []}
    resp = client.post("/patient/", json=new_patient)
    assert resp.status_code == 201
    assert resp.json()["id"] == "p3"

def test_update_patient():
    update = {"name": "Alice Updated", "age": 41, "allergies": ["Penicillin"], "prescriptions": ["rx1"]}
    resp = client.put("/patient/p1", json=update)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Alice Updated"

def test_delete_patient():
    resp = client.delete("/patient/p2")
    assert resp.status_code == 204
    # Should now 404
    resp2 = client.get("/patient/p2")
    assert resp2.status_code == 404

def test_list_prescriptions():
    resp = client.get("/patient/p1/prescriptions")
    assert resp.status_code == 200
    assert "rx1" in resp.json()

def test_get_allergies():
    resp = client.get("/patient/p1/allergies")
    assert resp.status_code == 200
    assert "Penicillin" in resp.json()

def test_update_allergies():
    resp = client.put("/patient/p1/allergies", json=["Aspirin"])
    assert resp.status_code == 200
    assert resp.json() == ["Aspirin"]
    # Confirm update
    resp2 = client.get("/patient/p1/allergies")
    assert resp2.json() == ["Aspirin"]
