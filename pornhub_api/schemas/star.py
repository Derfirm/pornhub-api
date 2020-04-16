from typing import List

from pydantic import BaseModel, AnyHttpUrl

__all__ = ("Star", "StarDetailed", "StarResult", "StarDetailedResult")


class Star(BaseModel):
    star_name: str


class StarDetailed(Star):
    star_url: AnyHttpUrl
    star_thumb: AnyHttpUrl
    gender: str
    videos_count_all: int


class StarResult(BaseModel):
    stars: List[Star]


class StarDetailedResult(BaseModel):
    stars: List[StarDetailed]
