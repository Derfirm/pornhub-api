from typing import List

from pydantic import BaseModel
from pydantic.fields import Field

from pornhub_api.schemas.video import Video


class VideoSearchResult(BaseModel):
    __root__: List[Video] = Field(..., alias="videos")

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def size(self):
        return len(self.__root__)
