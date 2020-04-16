from pydantic import AnyUrl, BaseModel

__all__ = ("Thumb",)


class Thumb(BaseModel):
    size: str
    width: str
    height: str
    src: AnyUrl
