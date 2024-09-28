import aiohttp


class AsyncHttpClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self._session = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None

    async def get(self, endpoint: str):
        async with self._session.get(f"{self.base_url}{endpoint}") as res:
            res.raise_for_status()
            return await res.json()
