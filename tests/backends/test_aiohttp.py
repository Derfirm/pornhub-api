import pytest
from aioresponses import aioresponses

from pornhub_api import PornhubApi
from pornhub_api.backends.aiohttp import AioHttpBackend

aiohttp = pytest.importorskip("aiohttp")


@pytest.fixture(params=["ph5c66d850c33de"])
def video_id(request):
    return request.param


@pytest.fixture()
def response_snapshot(request, load_fixture):
    return load_fixture(f"{request.param}.json")


@pytest.fixture
async def api():
    backend = AioHttpBackend()
    yield PornhubApi(backend=backend)
    await backend.close()


class TestBackend:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "response_snapshot", [pytest.lazy_fixture("video_id")], indirect=True
    )
    async def test_ok(self, api, response_snapshot, video_id):
        with aioresponses() as m:
            m.get(
                f"{api.video.BASE_URL}/is_video_active?id={video_id}",
                payload=response_snapshot,
            )
            response = await api.video.is_active(video_id)

            assert response
