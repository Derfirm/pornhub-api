import pytest

from _pytest.fixtures import SubRequest


@pytest.fixture(params=["ph5c66d850c33de", "ph6361a2b63a3e4", "ph59a86d7a6890b"])
def video_id(request):
    return request.param


@pytest.fixture(params=[pytest.lazy_fixture("video_id")])
def is_active_video_id(request: SubRequest) -> str:
    return f"is_active.{request.param}"


@pytest.mark.parametrize(
    "response_snapshot", [pytest.lazy_fixture("video_id")], indirect=True
)
def test_get_by_id(video_id, response_snapshot, api, requests_mock):
    requests_mock.get(
        f"{api.video.url_builder.BASE_URL}/video_by_id?id={video_id}",
        json=response_snapshot,
    )
    response = api.video.get_by_id(video_id)

    response_snapshot.assert_equal(response)


@pytest.mark.parametrize(
    "response_snapshot", [pytest.lazy_fixture("is_active_video_id")], indirect=True
)
def test_is_active(video_id, response_snapshot, api, requests_mock):
    requests_mock.get(
        f"{api.video.url_builder.BASE_URL}/is_video_active?id={video_id}",
        json=response_snapshot,
    )
    response = api.video.is_active(video_id)

    response_snapshot.assert_equal(response)
    assert response.video_id == video_id
    assert response.is_active


@pytest.mark.parametrize("response_snapshot", ["categories"], indirect=True)
def test_categories(response_snapshot, api, requests_mock):
    requests_mock.get(
        f"{api.video.url_builder.BASE_URL}/categories", json=response_snapshot
    )
    response = api.video.categories()

    response_snapshot.assert_equal(response)


@pytest.mark.parametrize("response_snapshot", ["tags.y"], indirect=True)
@pytest.mark.parametrize("tag", ["y"])
def test_tags(response_snapshot, api, requests_mock, tag):
    requests_mock.get(
        f"{api.video.url_builder.BASE_URL}/tags?list={tag}", json=response_snapshot
    )
    response = api.video.tags(tag)

    response_snapshot.assert_equal(response)
