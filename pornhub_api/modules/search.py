from typing import List, Union, Optional, Awaitable

from pornhub_api.modules.base import WebMasterUrlBuilder
from pornhub_api.backends.base import BackendT
from pornhub_api.schemas.search import VideoSearchResult

__all__ = ("Search",)


class Search:
    __slots__ = ("backend", "url_builder")

    def __init__(self, backend: BackendT):
        self.backend = backend
        self.url_builder = WebMasterUrlBuilder()

    def search_videos(
        self,
        q: str = "",
        *,
        thumbsize: str = "small",
        category: Optional[str] = None,
        page: int = 1,
        ordering: str = None,
        phrase: List[str] = None,
        tags: List[str] = None,
        period: str = None,
    ) -> Union[VideoSearchResult, Awaitable[VideoSearchResult]]:
        """
        :param q:
        :param page:
        :param ordering: Text. Possible values are featured, newest, mostviewed and rating
        :param thumbsize: Possible values are small,medium,large,small_hd,medium_hd,large_hd
        :param category:
        :param phrase: Array. Used as pornstars filter.
        :param tags:
        :param period: Text. Only works with ordering parameter. Possible values are weekly, monthly, and alltime
        :return: VideoSearchResult schema
        """
        url = self.url_builder.build_url("/search")
        params = {"search": q, "page": page, "thumbsize": thumbsize}

        if category is not None:
            params["category"] = category
        if ordering is not None:
            params["ordering"] = ordering
        if phrase is not None:
            params["phrase[]"] = ",".join(phrase)
        if tags is not None:
            params["tags[]"] = ",".join(tags)
        if period is not None and category is not None:
            params["period"] = period

        return self.backend.send_request(
            "get", url, params=params, response_schema=VideoSearchResult
        )
