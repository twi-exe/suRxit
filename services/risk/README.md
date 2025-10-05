# suRxit Clinical-Risk Engine

This service provides a unified API for evaluating prescription risk, including DDI, ADR, DFI, home-remedy guidance, and alternative drug recommendations.

## Endpoints
- `POST /predict/risk` — Evaluate prescription risk
- `GET /risk/{patient_id}` — Retrieve historical risk records
- `GET /risk/config` — Get risk thresholds/weights
- `PUT /risk/config` — Update config (admin)

See below for example request/response formats and usage.
