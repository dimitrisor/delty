from typing import Iterator, Any

import requests
from requests import Response


class WebClient:
    def get_response(
        self, url: str, check_crawlability: bool = False
    ) -> Iterator[Any] | Response:
        response = requests.get(url, stream=check_crawlability, verify=False)
        response.raise_for_status()
        if check_crawlability:
            return next(response.iter_content(10))
        return response
