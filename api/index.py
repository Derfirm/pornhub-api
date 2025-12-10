from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
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
# (We need to ensure api/redtube.py exists in the PYTHONPATH or relative import works)
try:
    from api.redtube import RedTubeApi
except ImportError:
    # Fallback for local run structure vs vercel structure
    try:
        from api.redtube import RedTubeApi
    except ImportError:
         sys.path.append(os.path.dirname(__file__))
         from api.redtube import RedTubeApi

app = FastAPI()

# Mount the public directory for static files (important for local dev)
public_path = os.path.join(os.path.dirname(__file__), '../public')
if not os.path.exists(public_path):
    # In Vercel, sometimes paths are tricky. Let's try to find public relative to current file.
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
    source: str = "pornhub" # pornhub, redtube, hybrid
):
    query = q if q else "4k"

    # Define tasks
    tasks = []

    # Task for Pornhub
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

    # Task for RedTube
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

        # Interleave results for a better hybrid experience
        # e.g. [ph1, rt1, ph2, rt2, ...]
        max_len = max(len(ph_res), len(rt_res))
        for i in range(max_len):
            if i < len(ph_res):
                results.append(ph_res[i])
            if i < len(rt_res):
                results.append(rt_res[i])
    else:
        # Default to PH
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

    else: # Default or explicitly Pornhub
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
                # Fallback: sometimes ID might be RedTube passed without source param?
                # But we should rely on client sending correct source.
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

# Catch-all route to serve the frontend for any non-api path
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    # If the request matches a file in public, serve it (fallback for when app.mount didn't catch it?)
    # But usually app.mount handles it if the path matches /public.
    # We want to serve index.html for root and unknown paths (SPA behavior)

    # Try to find the file
    possible_path = os.path.join(public_path, full_path)
    if os.path.isfile(possible_path):
        return FileResponse(possible_path)

    # Otherwise serve index.html
    index_path = os.path.join(public_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)

    return HTMLResponse(content="<h1>Frontend not found</h1>", status_code=404)
