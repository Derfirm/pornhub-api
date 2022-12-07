import pytest


@pytest.fixture(params=["ph5c66d850c33de"])
def video_id(request):
    return request.param
