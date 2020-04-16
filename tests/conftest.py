import json
from enum import Enum
from uuid import UUID
from decimal import Decimal
from pathlib import Path
from datetime import datetime

import pytest
from deepdiff import DeepDiff
from pydantic.networks import AnyUrl

from pornhub_api import PornhubApi


@pytest.fixture
def api():
    return PornhubApi()


@pytest.fixture(scope="module")
def load_fixture(request):
    class CompareDict(dict):
        def assert_equal(self, response):
            assert_response(response, dict(self))

    fixtures_dir: Path = Path(request.module.__file__).parent / "snapshots"

    def loader(fixture_name: str):
        with fixtures_dir.joinpath(fixture_name).open() as f:
            return CompareDict(json.load(f))

    return loader


def assert_response(response, expected_payload):
    def _normalize(value):
        if isinstance(value, UUID):
            return str(value)
        elif isinstance(value, datetime):
            return str(value)
        elif isinstance(value, Enum):
            return value.value
        elif isinstance(value, (Decimal, float)):
            return str(value)
        elif isinstance(value, AnyUrl):
            return str(value)
        elif value is None:
            return None
        else:
            return value

    def _process(data):
        _data = {}

        def _process_list(lst):
            tmp_list = []
            for v in lst:
                if isinstance(v, dict):
                    tmp_list.append(_process(v))
                elif isinstance(v, list):
                    tmp_list.append(_process_list(v))
                else:
                    tmp_list.append(_normalize(v))
            return tmp_list

        for key, value in data.items():
            if isinstance(value, dict):
                _data[key] = _process(value)
            elif isinstance(value, list):
                _data[key] = _process_list(value)
            else:
                _data[key] = _normalize(value)
        return _data

    response_type = response.__class__
    # try load payload
    tmp_data = response_type.parse_obj(expected_payload)
    tmp_data.dict()
    # normalize response
    actual_payload = _process(response.dict())
    # compare schema and data
    assert not DeepDiff(expected_payload, actual_payload)
