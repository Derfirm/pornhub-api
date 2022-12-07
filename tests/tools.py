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


if __name__ == "__main__":
    api = PornhubApi(RawBackend())
    result = api.search.search_videos(q="noway")
    save_snapshots(result, path="backends", tags=["noway"])
