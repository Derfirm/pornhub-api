from types import TracebackType
from typing import Any, Dict, Type, Optional

from pornhub_api.backends.base import BaseAsyncBackend
from httpx import AsyncClient

__all__ = ("AsyncHttpxBackend",)


class AsyncHttpxBackend(BaseAsyncBackend):
    __slots__ = ("AsyncClient",)

    def __init__(self):
        self._client = AsyncClient()

    async def __aenter__(self) -> "AsyncHttpxBackend":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ):
        await self.close()

    async def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        response = await self._client.request(method, url, **kwargs)
        response.raise_for_status()
        data = response.json()
        return data

    async def close(self):
        await self._client.aclose()
