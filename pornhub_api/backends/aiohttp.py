from types import TracebackType
from typing import Any, Dict, Type, Optional

from pornhub_api.backends.base import BaseAsyncBackend
import aiohttp

__all__ = ("AioHttpBackend",)


class AioHttpBackend(BaseAsyncBackend):
    def __init__(self):
        self._session = aiohttp.ClientSession()

    async def __aenter__(self) -> "AioHttpBackend":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ):
        await self.close()

    async def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        async with self._session.request(method, url, **kwargs) as response:
            response.raise_for_status()
            data = await response.json()
        return data

    async def close(self):
        await self._session.close()
