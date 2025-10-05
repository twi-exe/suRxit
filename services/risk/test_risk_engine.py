import pytest
from fastapi.testclient import TestClient


from services.risk.app import app
from fastapi import Depends
from services.risk.router_risk import oauth2_scheme

# Override OAuth2 dependency to always return a dummy token
app.dependency_overrides[oauth2_scheme] = lambda: "test-token"


# Patch all async service client methods to avoid real HTTP calls (including GNNDdiClient)
from services.risk import router_risk

async def dummy_get_patient_history(self, patient_id):
    return {"allergies": [], "conditions": []}

async def dummy_get_features(self, patient_id, drug_id):
    return {"features": [0.1, 0.2]}

async def dummy_get_adr_flags(self, patient_id, drug_id):
    return {"risk": 0.0}

async def dummy_get_dfi(self, drug_id):
    return []

async def dummy_get_home_remedies(self, drug_name):
    return [{"remedy": "rest", "description": "Get plenty of rest", "cautionary_note": "None", "confidence": 1.0}]

async def dummy_get_evidence_paths(self, drug1_id, drug2_id):
    return ["evidence_path1", "evidence_path2"]

async def dummy_get_alternatives(self, drug_id, patient_profile):
    return [{"drug_id": "alt1"}]

async def dummy_get_ddi(self, drug1_id, drug2_id):
    return {"risk": 1.0}

# Patch all clients globally for all tests
router_risk.KGClient.get_patient_history = dummy_get_patient_history
router_risk.KGClient.get_adr_flags = dummy_get_adr_flags
router_risk.KGClient.get_evidence_paths = dummy_get_evidence_paths
router_risk.FeatureGenClient.get_features = dummy_get_features
router_risk.DFIClient.get_dfi = dummy_get_dfi
router_risk.MedLMClient.get_home_remedies = dummy_get_home_remedies
router_risk.RecommenderClient.get_alternatives = dummy_get_alternatives
router_risk.GNNDdiClient.get_ddi = dummy_get_ddi

client = TestClient(app)

# --- Fixtures ---
@pytest.fixture
def sample_prescription():
    return {
        "patient_id": "patient123",
        "prescription": [
            {"drug_id": "drugA", "name": "Aspirin", "dose": "100mg", "freq": "OD", "duration": "5d"},
            {"drug_id": "drugB", "name": "Warfarin", "dose": "5mg", "freq": "OD", "duration": "7d"}
        ]
    }

# --- Test: DDI High Risk triggers alert and alternatives ---
def test_ddi_high_risk(sample_prescription):
    response = client.post("/predict/risk", json=sample_prescription)
    assert response.status_code == 200
    data = response.json()
    assert data["level"] in ("HIGH", "CRITICAL")
    assert data["recommendations"]

# --- Test: DFI caution always present if DFI exists ---
def test_dfi_caution(sample_prescription):
    # Patch DFIClient.get_dfi to return a DFI caution for this test
    orig = router_risk.DFIClient.get_dfi
    async def dfi_caution(self, drug_id):
        return [{"food_item": "grapefruit", "advice": "avoid", "type": "avoid", "reason": "CYP3A4 interaction"}]
    router_risk.DFIClient.get_dfi = dfi_caution
    response = client.post("/predict/risk", json=sample_prescription)
    router_risk.DFIClient.get_dfi = orig
    assert response.status_code == 200
    data = response.json()
    assert data["dfi_cautions"]
    assert any("grapefruit" in c["food_item"] for c in data["dfi_cautions"])

# --- Test: Home remedies always present ---
def test_home_remedies_present(sample_prescription):
    response = client.post("/predict/risk", json=sample_prescription)
    assert response.status_code == 200
    data = response.json()
    assert data["home_remedies"]

# --- Test: Alert trigger for high risk or DFI ---
def test_alert_trigger(sample_prescription):
    # Patch GNNDdiClient.get_ddi and DFIClient.get_dfi to trigger alert
    orig_ddi = router_risk.GNNDdiClient.get_ddi
    orig_dfi = router_risk.DFIClient.get_dfi
    async def high_ddi(self, d1, d2):
        return {"risk": 1.0}
    async def dfi_caution(self, drug_id):
        return [{"food_item": "milk", "advice": "limit", "type": "limit", "reason": "absorption"}]
    router_risk.GNNDdiClient.get_ddi = high_ddi
    router_risk.DFIClient.get_dfi = dfi_caution
    response = client.post("/predict/risk", json=sample_prescription)
    router_risk.GNNDdiClient.get_ddi = orig_ddi
    router_risk.DFIClient.get_dfi = orig_dfi
    assert response.status_code == 200
    data = response.json()
    assert data["level"] in ("HIGH", "CRITICAL") or data["dfi_cautions"]
