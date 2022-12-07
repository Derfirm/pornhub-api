__all__ = ("WebMasterUrlBuilder",)


class WebMasterUrlBuilder:
    BASE_URL = "https://www.pornhub.com/webmasters"

    def build_url(self, path: str) -> str:
        """
        >>> WebMasterUrlBuilder().build_url("/hello_world")
        'https://www.pornhub.com/webmasters/hello_world'
        """
        return f"{self.BASE_URL}{path}"
