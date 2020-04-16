__all__ = ("WebMasterUrlBuilder",)


class WebMasterUrlBuilder:
    BASE_URL = "http://www.pornhub.com/webmasters"

    def build_url(self, path: str) -> str:
        """
        >>> WebMasterUrlBuilder().build_url("/hello_world")
        "http://www.pornhub.com/webmasters/hello_worlds"

        :param path: end of endpont,
        :return: full url
        """
        return f"{self.BASE_URL}{path}"
