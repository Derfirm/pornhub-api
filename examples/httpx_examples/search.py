import asyncio
from typing import AsyncIterable

from pornhub_api import PornhubApi, exceptions
from pornhub_api.schemas.video import Video
from pornhub_api.backends.httpx import AsyncHttpxBackend
from pornhub_api.schemas.search import VideoSearchResult


async def find_video_by_word(
    word: str, backend: AsyncHttpxBackend, pages=5
) -> AsyncIterable[Video]:
    page = 1
    while page <= pages:
        api = PornhubApi(backend=backend)
        try:
            result: VideoSearchResult = await api.search.search_videos(
                q=word,
                page=page,
            )
        except exceptions.response.NoVideoError:
            break
        page += 1
        if not result.size():
            break
        for v in result:
            yield v


async def main() -> None:
    async with AsyncHttpxBackend() as backend:
        async for video in find_video_by_word("noway", backend=backend, pages=2):
            print(video.json())


if __name__ == "__main__":
    asyncio.run(main())
