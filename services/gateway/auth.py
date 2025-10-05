"""
auth.py — authentication and authorization

Responsibilities:
    - JWT authentication
    - RBAC (doctor, patient, admin)
    - API-key validation for internal ML-service calls
    - FastAPI dependency for routes
"""
from fastapi import FastAPI

def setup_auth(app: FastAPI):
        """Setup JWT, RBAC, and API-key middleware for FastAPI app."""
        # TODO: Implement JWT, RBAC, API-key logic
        pass
