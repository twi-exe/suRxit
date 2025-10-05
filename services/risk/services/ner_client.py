# NER client
import httpx

class NERClient:
    def __init__(self, base_url="http://ner:8000"):
        self.base_url = base_url

    async def extract_entities(self, text):
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.base_url}/extract", json={"text": text})
            resp.raise_for_status()
            return resp.json()
