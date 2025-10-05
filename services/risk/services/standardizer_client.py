# Standardizer client
import httpx

class StandardizerClient:
    def __init__(self, base_url="http://standardizer:8000"):
        self.base_url = base_url

    async def standardize(self, drug_name):
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.base_url}/standardize", json={"drug_name": drug_name})
            resp.raise_for_status()
            return resp.json()
