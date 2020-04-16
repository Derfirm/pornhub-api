import pytest


@pytest.fixture(params=["ph5c66d850c33de"])
def video_id(request):
    return request.param


@pytest.fixture()
def response_snapshot(request, load_fixture):
    return load_fixture(f"{request.param}.json")


@pytest.mark.parametrize(
    "response_snapshot", [pytest.lazy_fixture("video_id")], indirect=True
)
def test_get_by_id(video_id, response_snapshot, api, requests_mock):
    requests_mock.get(
        f"{api.video.BASE_URL}/video_by_id?id={video_id}", json=response_snapshot
    )
    response = api.video.get_by_id(video_id)

    response_snapshot.assert_equal(response)


@pytest.mark.parametrize(
    "response_snapshot", [f"is_active.ph5c66d850c33de"], indirect=True
)
def test_is_active(video_id, response_snapshot, api, requests_mock):
    requests_mock.get(
        f"{api.video.BASE_URL}/is_video_active?id={video_id}", json=response_snapshot
    )
    response = api.video.is_active(video_id)

    assert response


@pytest.mark.parametrize("response_snapshot", ["categories"], indirect=True)
def test_categories(response_snapshot, api, requests_mock):
    requests_mock.get(f"{api.video.BASE_URL}/categories", json=response_snapshot)
    response = api.video.categories()

    response_snapshot.assert_equal(response)


@pytest.mark.parametrize("response_snapshot", ["tags.y"], indirect=True)
@pytest.mark.parametrize("tag", ["y"])
def test_tags(response_snapshot, api, requests_mock, tag):
    requests_mock.get(f"{api.video.BASE_URL}/tags?list={tag}", json=response_snapshot)
    response = api.video.tags(tag)

    response_snapshot.assert_equal(response)
