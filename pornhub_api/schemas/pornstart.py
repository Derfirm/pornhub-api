from pydantic import BaseModel

__all__ = ("Pornstar",)


class Pornstar(BaseModel):
    pornstar_name: str
