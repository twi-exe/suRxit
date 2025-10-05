from fastapi import FastAPI
from .router_risk import router as risk_router

app = FastAPI(title="suRxit Clinical-Risk Engine")
app.include_router(risk_router)
