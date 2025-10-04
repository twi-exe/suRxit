import os
import shutil
import requests
from PIL import Image, ImageDraw

def create_sample_image(path):
    img = Image.new('RGB', (200, 60), color = (255,255,255))
    d = ImageDraw.Draw(img)
    d.text((10,10), "Paracetamol 500mg", fill=(0,0,0))
    img.save(path)

def test_round_trip_pipeline():
    # 1. Upload image to OCR
    sample_dir = 'data/uploads/test-pipeline/'
    os.makedirs(sample_dir, exist_ok=True)
    img_path = os.path.join(sample_dir, 'sample_rx.png')
    create_sample_image(img_path)
    with open(img_path, "rb") as f:
        ocr_resp = requests.post("http://localhost:8001/ocr/upload", files={"file": ("sample_rx.png", f, "image/png")})
    assert ocr_resp.status_code == 200
    ocr_data = ocr_resp.json()
    assert 'raw_text' in ocr_data
    ingest_id = ocr_data['ingest_id']

    # 2. Send text to NER
    ner_resp = requests.post("http://localhost:8002/ner/parse", json={"text": ocr_data['raw_text'], "ingest_id": ingest_id})
    assert ner_resp.status_code == 200
    ner_data = ner_resp.json()
    assert 'entities' in ner_data
    drug_entities = [e for e in ner_data['entities'] if e['type'].upper() == 'DRUG']
    assert drug_entities, "No drug entities found"

    # 3. Standardize entities
    std_req = {"entities": [{"text": e['text'], "type": e['type']} for e in drug_entities]}
    std_resp = requests.post("http://localhost:8003/standardize", json=std_req)
    assert std_resp.status_code == 200
    std_data = std_resp.json()
    assert 'results' in std_data
    found_canonical = any(r['canonical_id'] for r in std_data['results'])
    assert found_canonical, "No canonical drug ID returned"

    # Cleanup
    shutil.rmtree(sample_dir, ignore_errors=True)
    shutil.rmtree(os.path.join('data/uploads', ingest_id), ignore_errors=True)

if __name__ == "__main__":
    test_round_trip_pipeline()
    print("Round-trip pipeline test passed.")
