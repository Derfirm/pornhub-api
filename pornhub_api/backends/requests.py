from typing import Any, Dict

from pornhub_api.backends.base import BaseBackend
import requests

__all__ = ("RequestsBackend",)


class RequestsBackend(BaseBackend):
    def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        data = response.json()
        return data
