from typing import List

from pydantic import BaseModel

from pornhub_api.schemas.video import Video


class VideoSearchResult(BaseModel):
    videos: List[Video]

    def size(self):
        return len(self.videos)
