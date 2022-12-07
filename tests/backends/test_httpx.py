import pytest

from pornhub_api import PornhubApi
from pornhub_api.backends.httpx import AsyncHttpxBackend
import pytest_asyncio

httpx = pytest.importorskip("httpx")


@pytest_asyncio.fixture
async def api():
    async with AsyncHttpxBackend() as backend:
        yield PornhubApi(backend=backend)


class TestBackend:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "response_snapshot", [pytest.lazy_fixture("is_active_video_id")], indirect=True
    )
    async def test_ok(
        self, api: PornhubApi, response_snapshot, video_id: str, httpx_mock
    ):
        httpx_mock.add_response(
            url=f"{api.video.url_builder.BASE_URL}/is_video_active?id={video_id}",
            json=response_snapshot,
        )
        response = await api.video.is_active(video_id)

        response_snapshot.assert_equal(response)
