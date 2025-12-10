from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pornhub_api import PornhubApi
from pornhub_api.backends.aiohttp import AioHttpBackend
from typing import List, Optional, Dict, Any
import sys
import os
import asyncio
import random

# Ensure we can import from the root if needed
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import RedTube API
try:
    from api.redtube import RedTubeApi
except ImportError:
    try:
        from redtube import RedTubeApi
    except ImportError:
         sys.path.append(os.path.dirname(__file__))
         from redtube import RedTubeApi

app = FastAPI()

# Mount the public directory for static files
# In Vercel, the filesystem is read-only, but we can read included files.
public_path = os.path.join(os.path.dirname(__file__), '../public')
if not os.path.exists(public_path):
    public_path = os.path.join(os.getcwd(), 'public')

if os.path.exists(public_path):
    app.mount("/public", StaticFiles(directory=public_path), name="public")

@app.get("/api/search")
async def search_videos(
    q: str = Query(None, description="Search query"),
    page: int = 1,
    ordering: str = "mostviewed",
    period: str = "alltime",
    tags: Optional[List[str]] = Query(None),
    source: str = "pornhub"
):
    query = q if q else "4k"

    async def fetch_pornhub():
        async with AioHttpBackend() as backend:
            api = PornhubApi(backend=backend)
            try:
                kwargs = {
                    "q": query,
                    "page": page,
                    "ordering": ordering,
                    "period": period
                }
                if tags:
                    kwargs["tags"] = tags

                results = await api.search.search_videos(**kwargs)

                videos = []
                for vid in results:
                    videos.append({
                        "title": vid.title,
                        "video_id": vid.video_id,
                        "views": vid.views,
                        "rating": vid.rating,
                        "duration": vid.duration,
                        "thumb": str(vid.default_thumb) if vid.default_thumb else None,
                        "url": str(vid.url),
                        "source": "pornhub"
                    })
                return videos
            except Exception as e:
                print(f"Pornhub error: {e}")
                return []

    async def fetch_redtube():
        api = RedTubeApi()
        try:
            return await api.search_videos(
                q=query,
                page=page,
                ordering=ordering,
                period=period,
                tags=tags
            )
        except Exception as e:
            print(f"RedTube error: {e}")
            return []

    results = []

    if source == "pornhub":
        results = await fetch_pornhub()
    elif source == "redtube":
        results = await fetch_redtube()
    elif source == "hybrid":
        ph_res, rt_res = await asyncio.gather(fetch_pornhub(), fetch_redtube())
        max_len = max(len(ph_res), len(rt_res))
        for i in range(max_len):
            if i < len(ph_res):
                results.append(ph_res[i])
            if i < len(rt_res):
                results.append(rt_res[i])
    else:
        results = await fetch_pornhub()

    return {"videos": results, "count": len(results)}

@app.get("/api/video/{video_id}")
async def get_video_details(video_id: str, source: str = "pornhub"):
    if source == "redtube":
        api = RedTubeApi()
        vid = await api.get_video_by_id(video_id)
        if not vid:
            raise HTTPException(status_code=404, detail="Video not found")
        return vid
    else:
        async with AioHttpBackend() as backend:
            api = PornhubApi(backend=backend)
            try:
                vid = await api.video.get_by_id(video_id)
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
                    "embed_url": f"https://www.pornhub.com/embed/{vid.video_id}",
                    "source": "pornhub"
                }
            except Exception as e:
                raise HTTPException(status_code=404, detail="Video not found or API error")

@app.get("/api/tags")
async def get_tags(start: str = "a"):
    async with AioHttpBackend() as backend:
        api = PornhubApi(backend=backend)
        try:
            tags_result = await api.video.tags(start)
            return {"tags": tags_result.tags}
        except Exception as e:
             raise HTTPException(status_code=500, detail=str(e))

# Health Check
@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

# Catch-all for Frontend
@app.get("/{full_path:path}")
async def catch_all(full_path: str, request: Request):
    # If path starts with /api/, return 404 because it's a missing API route
    if full_path.startswith("api/"):
        return JSONResponse({"error": "Not Found"}, status_code=404)

    # Check for static file in public
    possible_path = os.path.join(public_path, full_path)
    if os.path.isfile(possible_path):
        return FileResponse(possible_path)

    # Default to index.html (SPA Fallback)
    index_path = os.path.join(public_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)

    return HTMLResponse(content="<h1>Error: Frontend not found.</h1>", status_code=500)
