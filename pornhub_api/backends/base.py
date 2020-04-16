from typing import Any

__all__ = ("Backend", "check_response")


class Backend:
    @staticmethod
    def send_request(method: str, url: str, **kwargs: Any) -> Any:
        raise NotImplementedError


def check_response(respose):
    data = respose.json()
    known_codes = {"1001", "1002", "1003", "2001", "2002", "3001", "3002", "3003"}
    if "code" in data and data["code"] in known_codes:
        raise ValueError(data)
