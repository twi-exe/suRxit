# KG (Knowledge Graph) client
import httpx

class KGClient:
    def __init__(self, base_url="http://kg:8000"):
        self.base_url = base_url

    async def get_patient_history(self, patient_id):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/patient/history", params={"patient_id": patient_id})
            resp.raise_for_status()
            return resp.json()

    async def get_adr_flags(self, patient_id, drug_id):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/adr", params={"patient_id": patient_id, "drug_id": drug_id})
            resp.raise_for_status()
            return resp.json()

    async def get_dfi(self, drug_id):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/dfi", params={"drug_id": drug_id})
            resp.raise_for_status()
            return resp.json()

    async def get_evidence_paths(self, drug1_id, drug2_id):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/evidence-paths", params={"drug1_id": drug1_id, "drug2_id": drug2_id})
            resp.raise_for_status()
            return resp.json()
