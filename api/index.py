from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pornhub_api import PornhubApi
from pornhub_api.backends.aiohttp import AioHttpBackend
from typing import List, Optional
import sys
import os

# Ensure we can import from the root if needed (though on Vercel dependencies are installed)
# But for local dev using the repo source:
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

app = FastAPI()

# Mount the public directory for static files (important for local dev)
# On Vercel, this is handled by vercel.json usually, but this helps local testing
public_path = os.path.join(os.path.dirname(__file__), '../public')
if os.path.exists(public_path):
    app.mount("/public", StaticFiles(directory=public_path), name="public")

@app.get("/")
async def read_root():
    # Serve the index.html for root requests (local dev convenience)
    return FileResponse(os.path.join(public_path, "index.html"))

@app.get("/api/search")
async def search_videos(
    q: str = Query(None, description="Search query"),
    page: int = 1,
    ordering: str = "mostviewed",
    period: str = "alltime",
    tags: Optional[List[str]] = Query(None)
):
    async with AioHttpBackend() as backend:
        api = PornhubApi(backend=backend)
        try:
            # If q is None, maybe just search for "4k" or something popular to fill the screen
            query = q if q else "4k"

            # search_videos args: q, page, ordering, period, tags, etc.
            # Note: tags argument in the library might expect a list or specific format

            kwargs = {
                "q": query,
                "page": page,
                "ordering": ordering,
                "period": period
            }
            if tags:
                kwargs["tags"] = tags

            results = await api.search.search_videos(**kwargs)

            # Convert results to a JSON-friendly format
            videos = []
            for vid in results:
                # The vid object has attributes like title, video_id, etc.
                # We construct a simple dict
                videos.append({
                    "title": vid.title,
                    "video_id": vid.video_id,
                    "views": vid.views,
                    "rating": vid.rating,
                    "duration": vid.duration,
                    "thumb": str(vid.default_thumb) if vid.default_thumb else None,
                    "url": str(vid.url)
                })

            return {"videos": videos, "count": len(videos)}
        except Exception as e:
            # print(e)
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/video/{video_id}")
async def get_video_details(video_id: str):
    async with AioHttpBackend() as backend:
        api = PornhubApi(backend=backend)
        try:
            vid = await api.video.get_by_id(video_id)

            # Construct response
            return {
                "title": vid.title,
                "video_id": vid.video_id,
                "views": vid.views,
                "rating": vid.rating,
                "duration": vid.duration,
                "thumb": str(vid.default_thumb),
                "thumbs": [str(t.src) for t in vid.thumbs] if vid.thumbs else [],
                "tags": [t.tag_name for t in vid.tags] if vid.tags else [],
                "categories": [c.category for c in vid.categories] if vid.categories else [],
                "pornstars": [p.pornstar_name for p in vid.pornstars] if vid.pornstars else [],
                "publish_date": vid.publish_date,
                # Embed URL is standard for PH
                "embed_url": f"https://www.pornhub.com/embed/{vid.video_id}"
            }
        except Exception as e:
            raise HTTPException(status_code=404, detail="Video not found or API error")

@app.get("/api/tags")
async def get_tags(start: str = "a"):
    # This might return a massive list, so maybe just top tags or by letter
    async with AioHttpBackend() as backend:
        api = PornhubApi(backend=backend)
        try:
            # The library has api.video.tags(literal)
            tags_result = await api.video.tags(start)
            return {"tags": tags_result.tags}
        except Exception as e:
             raise HTTPException(status_code=500, detail=str(e))
