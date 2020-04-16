from pornhub_api.schemas.tag import TagsResult
from pornhub_api.modules.base import WebMasterUrlBuilder
from pornhub_api.schemas.video import VideoResult
from pornhub_api.schemas.category import CategoriesResult

__all__ = ("Video",)


class Video(WebMasterUrlBuilder):
    __slots__ = ("backend",)

    def __init__(self, backend):
        self.backend = backend

    def get_by_id(self, id: str, *, thumbsize: str = "small",) -> VideoResult:
        """
        :param id: id of requested video
        :param thumbsize: (Optional)
        :return: Video schema
        """
        url = self.build_url("/video_by_id")

        params = {"id": id}
        if thumbsize is not None:
            params["thumbsize"] = thumbsize

        data = self.backend.send_request("get", url, params=params)
        return VideoResult(**data.json())

    def is_active(self, id: str) -> bool:
        url = self.build_url("/is_video_active")
        data = self.backend.send_request("get", url, params={"id": id}).json()
        assert data["active"]["video_id"] == id

        return bool(int(data["active"]["is_active"]))

    def categories(self) -> CategoriesResult:
        url = self.build_url("/categories")
        data = self.backend.send_request("get", url)
        return CategoriesResult(**data.json())

    def tags(self, literal: str):
        assert len(literal) == 1

        url = self.build_url("/tags")
        data = self.backend.send_request("get", url, params={"list": literal})
        return TagsResult(**data.json())
