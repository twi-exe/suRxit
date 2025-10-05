
"""
patient.py  /patient router

Endpoints:
	POST /patient/  Create patient
	GET /patient/  List patients
	GET /patient/{id}  Get patient
	PUT /patient/{id}  Update patient
	DELETE /patient/{id}  Delete patient
	GET /patient/{id}/prescriptions  List prescriptions
	GET/PUT /patient/{id}/allergies  Get/update allergies
"""
from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional

router = APIRouter()

# In-memory mock DB
MOCK_PATIENTS = {
	"p1": {"id": "p1", "name": "Alice", "age": 40, "allergies": ["Penicillin"], "prescriptions": ["rx1", "rx2"]},
	"p2": {"id": "p2", "name": "Bob", "age": 55, "allergies": [], "prescriptions": ["rx3"]},
}

@router.post("/", status_code=201)
def create_patient(patient: dict = Body(...)):
	if not patient.get("id") or patient["id"] in MOCK_PATIENTS:
		raise HTTPException(status_code=400, detail="Patient ID required and must be unique")
	MOCK_PATIENTS[patient["id"]] = patient
	return patient

@router.get("/", response_model=List[dict])
def list_patients():
	return list(MOCK_PATIENTS.values())

@router.get("/{id}")
def get_patient(id: str):
	patient = MOCK_PATIENTS.get(id)
	if not patient:
		raise HTTPException(status_code=404, detail="Patient not found")
	return patient

@router.put("/{id}")
def update_patient(id: str, patient: dict = Body(...)):
	if id not in MOCK_PATIENTS:
		raise HTTPException(status_code=404, detail="Patient not found")
	patient["id"] = id
	MOCK_PATIENTS[id] = patient
	return patient

@router.delete("/{id}", status_code=204)
def delete_patient(id: str):
	if id not in MOCK_PATIENTS:
		raise HTTPException(status_code=404, detail="Patient not found")
	del MOCK_PATIENTS[id]
	return

@router.get("/{id}/prescriptions")
def list_prescriptions(id: str):
	patient = MOCK_PATIENTS.get(id)
	if not patient:
		raise HTTPException(status_code=404, detail="Patient not found")
	return patient.get("prescriptions", [])

@router.get("/{id}/allergies")
def get_allergies(id: str):
	patient = MOCK_PATIENTS.get(id)
	if not patient:
		raise HTTPException(status_code=404, detail="Patient not found")
	return patient.get("allergies", [])

@router.put("/{id}/allergies")
def update_allergies(id: str, allergies: List[str] = Body(...)):
	patient = MOCK_PATIENTS.get(id)
	if not patient:
		raise HTTPException(status_code=404, detail="Patient not found")
	patient["allergies"] = allergies
	return allergies
