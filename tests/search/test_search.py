import pytest


@pytest.fixture(params=["beautiful", "pretty", "tagil", "empty"])
def search_q(request):
    return request.param


@pytest.mark.parametrize(
    "response_snapshot", [pytest.lazy_fixture("search_q")], indirect=True
)
def test_search_q(search_q, response_snapshot, requests_mock, api):
    requests_mock.get(
        f"{api.search.url_builder.BASE_URL}/search?search={search_q}&page=1&thumbsize=small",
        json=response_snapshot,
    )
    response = api.search.search_videos(search_q)

    response_snapshot.assert_equal(response)
    assert response.size() == len(response_snapshot["videos"])
