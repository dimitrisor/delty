from django.core.cache import cache

from delty.constants import CACHE_ADDRESS_TEXT, CACHE_ADDRESS_CONTENT_TYPE
from delty.services.crawler import CrawlerService
from delty.services.dom_processor import DomProcessor


def fetch_response(url: str) -> tuple[str, str]:
    if content := cache.get(CACHE_ADDRESS_TEXT.format(url)):
        content_type = cache.get(CACHE_ADDRESS_CONTENT_TYPE.format(url))
    else:
        response = CrawlerService().fetch_response(url)
        content = DomProcessor.convert_relative_to_absolute(
            base_url=url, html_content=response.text
        )
        content_type = response.headers.get("Content-Type")
        cache.set(
            CACHE_ADDRESS_TEXT.format(url),
            content,
            timeout=60 * 5,
        )
        cache.set(
            CACHE_ADDRESS_CONTENT_TYPE.format(url),
            content_type,
            timeout=60 * 5,
        )
    return content, content_type
