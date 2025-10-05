
"""
alerts.py  /alerts router

Endpoints:
	GET /alerts/  List alerts (filter by patient, status, time)
	GET /alerts/{alert_id}  Get alert details
"""
from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional

router = APIRouter()

# Mock in-memory alert data
MOCK_ALERTS = [
	{"id": "a1", "patient_id": "p1", "status": "unread", "type": "DDI", "created": "2025-10-01T10:00:00Z", "message": "Potential DDI detected."},
	{"id": "a2", "patient_id": "p2", "status": "read", "type": "ADR", "created": "2025-10-02T12:00:00Z", "message": "Possible ADR reported."},
	{"id": "a3", "patient_id": "p1", "status": "unread", "type": "DFI", "created": "2025-10-03T09:00:00Z", "message": "Dietary interaction risk."},
]

@router.get("/", response_model=List[dict])
def list_alerts(
	patient_id: Optional[str] = Query(None),
	status: Optional[str] = Query(None),
	alert_type: Optional[str] = Query(None),
	unread_only: Optional[bool] = Query(False)
):
	"""List alerts, filterable by patient, status, type, unread_only."""
	results = MOCK_ALERTS
	if patient_id:
		results = [a for a in results if a["patient_id"] == patient_id]
	if status:
		results = [a for a in results if a["status"] == status]
	if alert_type:
		results = [a for a in results if a["type"] == alert_type]
	if unread_only:
		results = [a for a in results if a["status"] == "unread"]
	return results

@router.get("/{alert_id}")
def get_alert(alert_id: str):
	"""Get alert details by ID."""
	for alert in MOCK_ALERTS:
		if alert["id"] == alert_id:
			return alert
	raise HTTPException(status_code=404, detail="Alert not found")
