import aiohttp
from typing import List, Optional, Dict, Any
import asyncio

class RedTubeApi:
    BASE_URL = "https://api.redtube.com/"

    def __init__(self):
        pass

    async def search_videos(
        self,
        q: str = "",
        page: int = 1,
        ordering: str = "newest",
        period: str = None,
        tags: List[str] = None
    ) -> List[Dict[str, Any]]:

        params = {
            "data": "redtube.Videos.searchVideos",
            "output": "json",
            "search": q,
            "page": page,
            "thumbsize": "medium"
        }

        if ordering:
            if ordering == "mostviewed":
                params["ordering"] = "mostviewed"
            elif ordering == "rating":
                params["ordering"] = "rating"
            elif ordering == "newest":
                params["ordering"] = "newest"

        if period:
             params["period"] = period

        if tags:
            params["tags"] = ",".join(tags)

        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status != 200:
                    return []

                try:
                    data = await response.json()
                except:
                    return []

                if "videos" not in data:
                    return []

                results = []
                for item in data["videos"]:
                    vid = item.get("video", {})
                    if not vid:
                        continue

                    results.append({
                        "title": vid.get("title"),
                        "video_id": vid.get("video_id"),
                        "views": int(vid.get("views", 0)) if vid.get("views") else 0,
                        "rating": float(vid.get("rating", 0)) if vid.get("rating") else 0.0,
                        "duration": vid.get("duration"),
                        "thumb": vid.get("default_thumb"),
                        "url": vid.get("url"),
                        "embed_url": vid.get("embed_url"),
                        "source": "redtube"
                    })

                return results

    async def get_video_by_id(self, video_id: str):
        params = {
            "data": "redtube.Videos.getVideo",
            "output": "json",
            "video_id": video_id
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status != 200:
                    return None

                try:
                    data = await response.json()
                except:
                    return None

                vid = data.get("video")
                if not vid:
                    return None

                return {
                    "title": vid.get("title"),
                    "video_id": vid.get("video_id"),
                    "views": int(vid.get("views", 0)) if vid.get("views") else 0,
                    "rating": float(vid.get("rating", 0)) if vid.get("rating") else 0.0,
                    "duration": vid.get("duration"),
                    "thumb": vid.get("default_thumb"),
                    "thumbs": [t.get("src") for t in vid.get("thumbs", [])],
                    "tags": [t.get("tag_name") for t in vid.get("tags", [])],
                    "categories": [],
                    "pornstars": [],
                    "publish_date": vid.get("publish_date"),
                    "embed_url": vid.get("embed_url"),
                    "source": "redtube"
                }
