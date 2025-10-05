# GNN-DDI client
import httpx

class GNNDdiClient:
    def __init__(self, base_url="http://gnn-ddi:8000"):
        self.base_url = base_url

    async def get_ddi(self, drug1_id, drug2_id):
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.base_url}/predict", json={"drug1_id": drug1_id, "drug2_id": drug2_id})
            resp.raise_for_status()
            return resp.json()
