import json
from typing import Any, Dict, List

from pornhub_api import PornhubApi
import requests


class RawBackend:
    # used only for update snapshots
    def send_request(
        self, method: str, url: str, response_schema: Any, **kwargs: Any
    ) -> Dict[str, Any]:
        response_data = requests.request(method, url, **kwargs)
        return response_data.json()


def save_snapshots(data: Dict[str, Any], path: str, tags: List[str]):
    with open(f"{path}/snapshots/{'.'.join(tags)}.json", "w") as fd:
        json.dump(data, fd)


def video_download(phub_api: PornhubApi, video_id: str):
    save_snapshots(
        phub_api.video.is_active(video_id), path="video", tags=["is_active", video_id]
    )
    save_snapshots(phub_api.video.get_by_id(video_id), path="video", tags=[video_id])


if __name__ == "__main__":
    api = PornhubApi(RawBackend())
    video_download(api, "ph59a86d7a6890b")
