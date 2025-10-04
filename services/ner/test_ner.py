from fastapi.testclient import TestClient
from main import app

def test_ner_parse():
    client = TestClient(app)
    text = "Patient is allergic to penicillin and takes Paracetamol 500mg twice daily for fever."
    ingest_id = "test-ingest-123"
    response = client.post("/ner/parse", json={"text": text, "ingest_id": ingest_id})
    assert response.status_code == 200
    data = response.json()
    assert 'entities' in data
    assert isinstance(data['entities'], list)
    # At least one entity should be present
    assert any(ent['type'] for ent in data['entities'])
    # All entities should have ingest_id
    for ent in data['entities']:
        assert ent['ingest_id'] == ingest_id
