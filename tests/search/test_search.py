import pytest


@pytest.fixture(params=["beautiful", "pretty", "tagil", "empty"])
def search_q(request):
    return request.param


@pytest.fixture()
def response_snapshot(search_q, load_fixture):
    return load_fixture(f"{search_q}.json")


@pytest.mark.parametrize(
    "response_snapshot", ["beautiful", "pretty", "tagil", "empty"], indirect=True
)
def test_search_q(search_q, response_snapshot, requests_mock, api):
    requests_mock.get(
        f"{api.search.url_builder.BASE_URL}/search?search={search_q}&page=1&thumbsize=small",
        json=response_snapshot,
    )
    response = api.search.search_videos(search_q)

    response_snapshot.assert_equal(response)
