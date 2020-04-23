from pornhub_api.schemas.tag import TagsResult
from pornhub_api.modules.base import WebMasterUrlBuilder
from pornhub_api.schemas.video import VideoResult, IsVideoActiveResult
from pornhub_api.schemas.category import CategoriesResult

__all__ = ("Video",)


class Video(WebMasterUrlBuilder):
    __slots__ = ("backend",)

    def __init__(self, backend):
        self.backend = backend

    def get_by_id(self, id_: str, *, thumbsize: str = None) -> VideoResult:
        """
        :param id_: id of requested video
        :param thumbsize: (Optional)
        :return: Video schema
        """
        url = self.build_url("/video_by_id")

        params = {"id": id_}
        if thumbsize is not None:
            params["thumbsize"] = thumbsize

        return self.backend.send_request(
            "get", url, params=params, response_schema=VideoResult
        )

    def is_active(self, id_: str) -> IsVideoActiveResult:
        url = self.build_url("/is_video_active")
        return self.backend.send_request(
            "get", url, params={"id": id_}, response_schema=IsVideoActiveResult
        )

    def categories(self) -> CategoriesResult:
        url = self.build_url("/categories")
        return self.backend.send_request("get", url, response_schema=CategoriesResult)

    def tags(self, literal: str):
        assert len(literal) == 1

        url = self.build_url("/tags")
        return self.backend.send_request(
            "get", url, params={"list": literal}, response_schema=TagsResult
        )
