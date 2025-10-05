# FeatureGen client
import httpx

class FeatureGenClient:
    def __init__(self, base_url="http://featuregen:8000"):
        self.base_url = base_url

    async def get_features(self, patient_id, drug_id):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/features", params={"patient_id": patient_id, "drug_id": drug_id})
            resp.raise_for_status()
            return resp.json()
