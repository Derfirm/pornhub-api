from typing import Any, List, Union
from datetime import datetime

from pydantic import Field, BaseModel, AnyHttpUrl, validator

from pornhub_api.schemas.tag import Tag
from pornhub_api.schemas.thumb import Thumb
from pornhub_api.schemas.pornstart import Pornstar

__all__ = ("Video", "VideoResult", "Category", "IsVideoActiveResult")


class Category(BaseModel):
    category: str


class Video(BaseModel):
    title: str
    duration: str
    views: int
    video_id: str
    rating: Union[float, int]
    ratings: int
    url: AnyHttpUrl
    default_thumb: AnyHttpUrl
    thumb: AnyHttpUrl
    publish_date: datetime
    segment: str
    thumbs: List[Thumb]
    tags: List[Tag]
    categories: List[Category]
    pornstars: List[Pornstar]

    @validator("rating")
    def prettify_float(cls, value: Union[float, int]) -> Union[float, int]:  # type: ignore
        if value == int(value):
            return int(value)
        return value


class VideoResult(BaseModel):
    __root__: Video = Field(..., alias="video")

    def __getattr__(self, item):
        return getattr(self.__root__, item)


class IsVideoActiveResult(BaseModel):
    class _Active(BaseModel):
        video_id: str
        is_active: str

    __root__: _Active = Field(..., alias="active")

    def __getattr__(self, item: Any) -> Any:
        return getattr(self.__root__, item)
