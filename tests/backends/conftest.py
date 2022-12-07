import pytest

from pytest_asyncio.plugin import SubRequest


@pytest.fixture(params=["ph5c66d850c33de"])
def video_id(request):
    return request.param


@pytest.fixture(params=[pytest.lazy_fixture("video_id")])
def is_active_video_id(request: SubRequest) -> str:
    return f"is_active.{request.param}"
