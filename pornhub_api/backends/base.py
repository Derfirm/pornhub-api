from typing import Any, Dict, Type, Union, Generic, TypeVar, Awaitable, overload

from pydantic import BaseModel

from pornhub_api.exceptions.response import parse_error

R = TypeVar("R", bound=BaseModel)

__all__ = ("BaseBackend", "BaseAsyncBackend", "check_response", "BackendT")


def _transform_response_into_model(data: Dict[str, Any], response_schema: Type[R]) -> R:
    return response_schema(**data)


class BaseBackend:
    def send_request(
        self, method: str, url: str, response_schema: Type[R], **kwargs: Any
    ) -> R:
        response_data = self._make_request(method, url, **kwargs)
        check_response(response_data)
        return _transform_response_into_model(response_data, response_schema)

    def _make_request(self, method: str, url: str, **kwargs: Any) -> Dict[str, Any]:
        raise NotImplementedError


class BaseAsyncBackend:
    async def send_request(
        self, method: str, url: str, response_schema: Type[R], **kwargs: Any
    ) -> R:
        response_data = await self._make_request(method, url, **kwargs)
        check_response(response_data)
        return _transform_response_into_model(response_data, response_schema)

    async def _make_request(
        self, method: str, url: str, **kwargs: Any
    ) -> Dict[str, Any]:
        raise NotImplementedError


BackendT = TypeVar("BackendT", bound=Union[BaseBackend, BaseAsyncBackend])


def check_response(data):
    known_codes = {
        "1001",
        "1002",
        "1003",
        "2000",
        "2001",
        "2002",
        "3001",
        "3002",
        "3003",
    }
    if "code" in data and data["code"] in known_codes:
        exception = parse_error(data)
        if exception:
            raise exception
        raise ValueError(data)
