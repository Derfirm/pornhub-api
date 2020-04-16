from typing import List, Optional

from pornhub_api.modules.base import WebMasterUrlBuilder
from pornhub_api.schemas.search import VideoSearchResult

__all__ = ("Search",)


class Search(WebMasterUrlBuilder):
    __slots__ = ("backend",)

    def __init__(self, backend):
        self.backend = backend

    def search(
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
    ) -> VideoSearchResult:
        """
        :param q:
        :param page:
        :param ordering: Text. Possible values are featured, newest, mostviewed and rating
        :param thumbsize: Possible values are small,medium,large,small_hd,medium_hd,large_hd
        :param category:
        :param phrase: Array. Used as pornstars filter.
        :param tags:
        :param period: Text. Only works with ordering parameter. Possible values are weekly, monthly, and alltime
        :return:
        """
        url = self.build_url("/search")
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

        data = self.backend.send_request("get", url, params=params)
        return VideoSearchResult(**data.json())
