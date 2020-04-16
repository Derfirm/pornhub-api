from typing import List

from pydantic import BaseModel

__all__ = ("Tag", "TagsResult")


class Tag(BaseModel):
    tag_name: str


class TagsResult(BaseModel):
    tags: List[str]
    tagsCount: int
