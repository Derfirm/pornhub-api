import pytest


@pytest.fixture(params=["ph5c66d850c33de"])
def video_id(request):
    return request.param


@pytest.fixture()
def response_snapshot(request, load_fixture):
    return load_fixture(f"{request.param}.json")
