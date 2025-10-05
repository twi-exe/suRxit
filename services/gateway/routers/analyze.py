
"""
analyze.py — /analyze router

Endpoints:
  POST /analyze/prescription
    - Accepts: prescription image, patient_id
    - Pipeline: OCR → NER → FeatureGen → Risk-Engine
    - Returns: unified risk response
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
import httpx
import os
import asyncio

router = APIRouter()

# Service URLs (could be moved to config/env)
OCR_URL = os.getenv("OCR_URL", "http://ocr:8000/ocr")
NER_URL = os.getenv("NER_URL", "http://ner:8000/extract")
FEATUREGEN_URL = os.getenv("FEATUREGEN_URL", "http://featuregen:8000/features")
RISK_URL = os.getenv("RISK_URL", "http://risk:8000/predict/risk")

async def default_http_client():
  async with httpx.AsyncClient() as client:
    yield client

@router.post("/prescription")
async def analyze_prescription(
  file: UploadFile = File(...),
  patient_id: str = Form(...),
  token: str = Depends(lambda: None),  # TODO: JWT auth
  http_client=Depends(default_http_client)
):
  """
  Orchestrate the full pipeline:
    1. OCR: extract text from image
    2. NER: extract drugs from text
    3. FeatureGen: get features for each drug
    4. Risk-Engine: get risk assessment
  Returns unified response.
  """
  ocr_resp = await http_client.post(OCR_URL, files={"file": (file.filename, await file.read(), file.content_type)})
  if ocr_resp.status_code != 200:
    raise HTTPException(status_code=502, detail="OCR service error")
  ocr_text = ocr_resp.json().get("text")

  ner_resp = await http_client.post(NER_URL, json={"text": ocr_text})
  if ner_resp.status_code != 200:
    raise HTTPException(status_code=502, detail="NER service error")
  drugs = ner_resp.json().get("drugs", [])

  feature_tasks = [http_client.get(FEATUREGEN_URL, params={"patient_id": patient_id, "drug_id": d["drug_id"]}) for d in drugs]
  feature_results = await asyncio.gather(*feature_tasks)
  features = [fr.json() for fr in feature_results if fr.status_code == 200]

  prescription = [{"drug_id": d["drug_id"], "name": d["name"], "dose": d.get("dose", ""), "freq": d.get("freq", ""), "duration": d.get("duration", "")} for d in drugs]
  risk_payload = {"patient_id": patient_id, "prescription": prescription}
  risk_resp = await http_client.post(RISK_URL, json=risk_payload)
  if risk_resp.status_code != 200:
    raise HTTPException(status_code=502, detail="Risk-Engine error")
  risk_result = risk_resp.json()

  return {
    "ocr_text": ocr_text,
    "drugs": drugs,
    "features": features,
    "risk": risk_result
  }
