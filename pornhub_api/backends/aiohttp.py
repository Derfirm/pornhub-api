import aiohttp

from pornhub_api.backends.base import Backend, check_response

__all__ = ("AioHttpBackend",)


class AioHttpBackend(Backend):
    def __init__(self):
        self._session = aiohttp.ClientSession()

    async def send_request(self, method: str, url: str, response_schema, **kwargs):
        async with self._session.request(method, url, **kwargs) as response:
            response.raise_for_status()
            data = await response.json()

        check_response(data)
        return response_schema(**data)

    async def close(self):
        await self._session.close()
