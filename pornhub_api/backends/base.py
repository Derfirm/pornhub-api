from typing import Any, Type, Generic, TypeVar

from pydantic import BaseModel

R = TypeVar("R", bound=BaseModel)

__all__ = ("Backend", "check_response")


class Backend(Generic[R]):
    def send_request(
        self, method: str, url: str, response_schema: Type[R], **kwargs: Any
    ) -> R:
        raise NotImplementedError


def check_response(data):
    known_codes = {"1001", "1002", "1003", "2001", "2002", "3001", "3002", "3003"}
    if "code" in data and data["code"] in known_codes:
        raise ValueError(data)
