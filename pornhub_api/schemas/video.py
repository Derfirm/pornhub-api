from typing import List
from datetime import datetime

from pydantic import BaseModel, AnyHttpUrl

from pornhub_api.schemas.tag import Tag
from pornhub_api.schemas.thumb import Thumb
from pornhub_api.schemas.category import Category
from pornhub_api.schemas.pornstart import Pornstar

__all__ = ("Video", "VideoResult")


class Video(BaseModel):
    title: str
    duration: str
    views: int
    video_id: str
    rating: float
    ratings: int
    url: AnyHttpUrl
    default_thumb: AnyHttpUrl
    thumb: AnyHttpUrl
    publish_date: datetime
    thumbs: List[Thumb]
    tags: List[Tag]
    categories: List[Category]
    pornstars: List[Pornstar]


class VideoResult(BaseModel):
    video: Video
