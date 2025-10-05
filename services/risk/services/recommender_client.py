# Recommender client
import httpx

class RecommenderClient:
    def __init__(self, base_url="http://recommender:8000"):
        self.base_url = base_url

    async def get_alternatives(self, drug_id, patient_profile):
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.base_url}/recommend", json={"drug_id": drug_id, "profile": patient_profile})
            resp.raise_for_status()
            return resp.json()
