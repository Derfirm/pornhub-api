from typing import Any, Dict, Optional

from pydantic import BaseModel

__all__ = ("NoVideoError",)


class BaseResponseError(Exception):
    def __init__(self, code: str, message: str, example: str) -> None:
        self.response_code = code
        self.response_message = message
        self.response_example = example


class NoVideoError(BaseResponseError):
    pass


class InvalidCategoryError(BaseResponseError):
    pass


# map code into known error class
error_mapping = {
    "2000": InvalidCategoryError,
    "2001": NoVideoError,
}


class _ErrorParser(BaseModel):
    code: str
    message: str
    example: str


def parse_error(data: Dict[str, Any]) -> Optional[BaseResponseError]:
    if data["code"] in error_mapping:
        error = _ErrorParser.parse_obj(data)
        exception_type = error_mapping[data["code"]]
        return exception_type(
            code=error.code, message=error.message, example=error.example
        )
    return None
