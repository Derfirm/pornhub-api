from typing import Union, Awaitable

from pornhub_api.modules.base import WebMasterUrlBuilder
from pornhub_api.schemas.star import StarResult, StarDetailedResult
from pornhub_api.backends.base import BackendT

__all__ = ("Stars",)


class Stars:
    __slots__ = ("backend", "url_builder")

    def __init__(self, backend: BackendT):
        """
        gather available stars list
        :param backend: request library
        """
        self.backend = backend
        self.url_builder = WebMasterUrlBuilder()

    def all(self) -> Union[StarResult, Awaitable[StarResult]]:
        url = self.url_builder.build_url("/stars")
        return self.backend.send_request("get", url, response_schema=StarResult)

    def all_detailed(self) -> Union[StarDetailedResult, Awaitable[StarDetailedResult]]:
        url = self.url_builder.build_url("/stars_detailed")
        return self.backend.send_request("get", url, response_schema=StarDetailedResult)
