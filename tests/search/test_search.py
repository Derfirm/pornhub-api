import pytest


@pytest.fixture(params=["beautiful", "pretty", "tagil", "empty"])
def search_q(request):
    return request.param


@pytest.fixture()
def response_snapshot(search_q, load_fixture):
    return load_fixture(f"{search_q}.json")


def test_search_q(search_q, response_snapshot, requests_mock, api):
    requests_mock.get(
        f"{api.search.BASE_URL}/search?search={search_q}&page=1&thumbsize=small",
        json=response_snapshot,
    )
    response = api.search.search(search_q)

    response_snapshot.assert_equal(response)
