import pytest

from pornhub_api import PornhubApi
from pornhub_api.backends.httpx import AsyncHttpxBackend
from pornhub_api.schemas.search import VideoSearchResult
from pornhub_api.backends.aiohttp import AioHttpBackend
import pytest_asyncio
from _pytest.fixtures import SubRequest


@pytest_asyncio.fixture()
async def aiohttp_backend() -> AioHttpBackend:
    async with AioHttpBackend() as backend:
        yield backend


@pytest_asyncio.fixture()
async def httpx_backend() -> AsyncHttpxBackend:
    async with AsyncHttpxBackend() as backend:
        yield backend


@pytest_asyncio.fixture(
    params=[
        pytest.lazy_fixture("aiohttp_backend"),
        pytest.lazy_fixture("httpx_backend"),
    ]
)
def api(request: SubRequest):
    return PornhubApi(request.param)


@pytest.mark.asyncio
@pytest.mark.webtest
async def test_api_call(api: PornhubApi):
    result: VideoSearchResult = await api.search.search_videos(q="qiwi")

    assert result
