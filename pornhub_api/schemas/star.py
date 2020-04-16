from typing import List

from pydantic import BaseModel, AnyHttpUrl

__all__ = ("StarSchema", "StarDetailedSchema", "StarResult", "StarDetailedResult")


class StarSchema(BaseModel):
    class Star(BaseModel):
        star_name: str

    star: Star


class StarDetailedSchema(BaseModel):
    class StarDetailed(BaseModel):
        star_name: str
        star_url: AnyHttpUrl
        star_thumb: AnyHttpUrl
        gender: str
        videos_count_all: str

    star: StarDetailed


class StarResult(BaseModel):
    stars: List[StarSchema]


class StarDetailedResult(BaseModel):
    stars: List[StarDetailedSchema]
