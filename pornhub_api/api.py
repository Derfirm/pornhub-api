from pornhub_api.modules.stars import Stars
from pornhub_api.modules.video import Video
from pornhub_api.modules.search import Search

__all__ = ("PornhubApi",)


class PornhubApi:
    def __init__(self, backend=None):
        if backend is None:
            from pornhub_api.backends.requests import RequestsBackend

            backend = RequestsBackend()

        self.backend = backend

    @property
    def search(self):
        return Search(backend=self.backend)

    @property
    def video(self):
        return Video(backend=self.backend)

    @property
    def stars(self):
        return Stars(backend=self.backend)

    def __str__(self):
        return f"<{self.__class__.__name__} with backend {self.backend.__class__.__name__}>"
