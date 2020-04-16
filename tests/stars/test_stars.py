import pytest


@pytest.fixture()
def response_snapshot(request, load_fixture):
    return load_fixture(f"{request.param}.json")


@pytest.mark.parametrize("response_snapshot", ["stars"], indirect=True)
def test_stars(response_snapshot, api, requests_mock):
    requests_mock.get(f"{api.stars.BASE_URL}/stars", json=response_snapshot)
    response = api.stars.all()

    response_snapshot.assert_equal(response)


@pytest.mark.parametrize("response_snapshot", ["stars_detailed"], indirect=True)
def test_stars_detailed(response_snapshot, api, requests_mock):
    requests_mock.get(f"{api.stars.BASE_URL}/stars_detailed", json=response_snapshot)
    response = api.stars.all_detailed()

    response_snapshot.assert_equal(response)
