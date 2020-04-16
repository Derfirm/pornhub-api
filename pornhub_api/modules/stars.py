from pornhub_api.modules.base import WebMasterUrlBuilder
from pornhub_api.schemas.star import StarResult, StarDetailedResult

__all__ = ("Stars",)


class Stars(WebMasterUrlBuilder):
    __slots__ = ("backend",)

    def __init__(self, backend):
        self.backend = backend

    def all(self) -> StarResult:
        url = self.build_url("/stars")
        data = self.backend.send_request("get", url)
        return StarResult(**data.json())

    def all_detailed(self) -> StarDetailedResult:
        url = self.build_url("/stars_detailed")
        data = self.backend.send_request("get", url)
        return StarDetailedResult(**data.json())
