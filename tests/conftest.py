import json
from enum import Enum
from uuid import UUID
from decimal import Decimal
from pathlib import Path
from datetime import datetime

import pytest
from pydantic.networks import AnyUrl

from pornhub_api import PornhubApi
from deepdiff import DeepDiff
from _pytest.fixtures import SubRequest


@pytest.fixture
def api():
    return PornhubApi()


@pytest.fixture(scope="module")
def load_fixture(request: SubRequest):
    class CompareDict(dict):
        def assert_equal(self, response):
            assert_response(response, dict(self))

    fixtures_dir: Path = Path(request.module.__file__).parent / "snapshots"

    def loader(fixture_name: str):
        with fixtures_dir.joinpath(fixture_name).open() as f:
            return CompareDict(json.load(f))

    return loader


@pytest.fixture()
def response_snapshot(request: SubRequest, load_fixture):
    return load_fixture(f"{request.param}.json")


def assert_response(response, expected_payload):
    response_type = response.__class__
    # try load payload
    tmp_data = response_type(**expected_payload)
    assert response.dict(by_alias=True) == tmp_data.dict(by_alias=True)
    # normalize response
    actual_payload = dict(_process(response.dict(by_alias=True)))
    # compare schema and data
    assert not DeepDiff(dict(_process(expected_payload)), actual_payload)


def _normalize(value):
    if isinstance(value, Enum):
        return value.value
    elif isinstance(value, (Decimal, int, float, UUID, datetime, AnyUrl)):
        return str(value)
    return value


def _process(data):
    def _process_list(lst):
        for v in lst:
            if isinstance(v, dict):
                yield dict(_process(v))
            elif isinstance(v, list):
                yield list(_process_list(v))
            else:
                yield _normalize(v)

    for key, value in data.items():
        if isinstance(value, dict):
            yield key, dict(_process(value))
        elif isinstance(value, list):
            yield key, list(_process_list(value))
        else:
            yield key, _normalize(value)
