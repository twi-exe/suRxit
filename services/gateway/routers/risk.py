
"""
risk.py /risk router

Endpoints:
  Proxy all /risk/* requests to Risk-Engine microservice.
  - GET /risk/{patient_id}
  - POST /risk/config
  - etc.
"""
from fastapi import APIRouter, Request, Response, status
import httpx
import os

router = APIRouter()
RISK_ENGINE_URL = os.getenv("RISK_ENGINE_URL", "http://risk:8000")

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_risk(request: Request, path: str):
	"""
	Proxy all /risk/* requests to the Risk-Engine microservice.
	Forwards method, headers, query params, and body.
	"""
	url = f"{RISK_ENGINE_URL}/{path}"
	method = request.method
	headers = dict(request.headers)
	params = dict(request.query_params)
	try:
		body = await request.body()
		async with httpx.AsyncClient() as client:
			resp = await client.request(
				method,
				url,
				headers={k: v for k, v in headers.items() if k.lower() != "host"},
				params=params,
				content=body if body else None,
			)
		return Response(
			content=resp.content,
			status_code=resp.status_code,
			headers={k: v for k, v in resp.headers.items() if k.lower() not in ["content-encoding", "transfer-encoding", "connection"]},
			media_type=resp.headers.get("content-type")
		)
	except httpx.RequestError as e:
		return Response(
			content=f"Risk-Engine unavailable: {str(e)}",
			status_code=status.HTTP_502_BAD_GATEWAY
		)
