import requests

from pornhub_api.backends.base import Backend, check_response

__all__ = ("RequestsBackend",)


class RequestsBackend(Backend):
    @staticmethod
    def send_request(method: str, url: str, **kwargs):
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        data = response
        check_response(response)
        return data
