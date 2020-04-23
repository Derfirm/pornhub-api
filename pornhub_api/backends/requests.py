import requests

from pornhub_api.backends.base import Backend, check_response

__all__ = ("RequestsBackend",)


class RequestsBackend(Backend):
    def send_request(self, method: str, url: str, response_schema, **kwargs):
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        data = response.json()
        check_response(data)
        return response_schema.parse_obj(data)
