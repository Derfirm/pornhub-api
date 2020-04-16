from typing import List

from pydantic import BaseModel

__all__ = ("Category", "CategoriesResult")


class Category(BaseModel):
    category: str


class CategoriesResult(BaseModel):
    categories: List[Category]
