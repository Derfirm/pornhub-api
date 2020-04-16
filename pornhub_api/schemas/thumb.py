from pydantic import AnyUrl, BaseModel

__all__ = ("Thumb",)


class Thumb(BaseModel):
    size: str
    width: int
    height: int
    src: AnyUrl
