import asyncio
from typing import AsyncIterable

from pornhub_api import PornhubApi, exceptions
from pornhub_api.schemas.video import Video
from pornhub_api.schemas.search import VideoSearchResult
from pornhub_api.backends.aiohttp import AioHttpBackend


async def find_video_by_world(
    word: str, backend: AioHttpBackend, pages=5
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
    async with AioHttpBackend() as backend:
        async for video in find_video_by_world("faines", backend=backend):
            print(video.title)


if __name__ == "__main__":
    asyncio.run(main())
