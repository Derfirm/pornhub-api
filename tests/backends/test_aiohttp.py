import pytest

from pornhub_api import PornhubApi
from pornhub_api.backends.aiohttp import AioHttpBackend
import pytest_asyncio
from aioresponses import aioresponses

aiohttp = pytest.importorskip("aiohttp")


@pytest_asyncio.fixture
async def api():
    async with AioHttpBackend() as backend:
        yield PornhubApi(backend=backend)


class TestBackend:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "response_snapshot", [pytest.lazy_fixture("video_id")], indirect=True
    )
    async def test_ok(self, api, response_snapshot, video_id):
        with aioresponses() as m:
            m.get(
                f"{api.video.url_builder.BASE_URL}/is_video_active?id={video_id}",
                payload=response_snapshot,
            )
            response = await api.video.is_active(video_id)

            assert response
