import httpx

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

async def fetch_via_http(url: str) -> str:
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
