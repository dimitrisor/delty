from django.core.cache import cache
from playwright.sync_api import sync_playwright

from delty.constants import (
    CACHE_ADDRESS_CONTENT_TYPE,
    CACHE_ADDRESS_STATIC_BODY,
    CACHE_ADDRESS_FULLY_LOADED_BODY,
)
from delty.services.crawler import CrawlerService
from delty.services.dom_processor import DomProcessor


def fetch_response_fully_loaded(
    url: str, iframe_width: int, iframe_height: int, user_agent: str
) -> tuple[str, str]:
    """
    On behalf of the browser the page was initially rendered in, fetch the body of the given URL after the page is
    fully loaded and the Javascript has run.
    """
    if content := cache.get(CACHE_ADDRESS_FULLY_LOADED_BODY.format(url)):
        content_type = cache.get(CACHE_ADDRESS_CONTENT_TYPE.format(url))
    else:
        with sync_playwright() as p:
            # Launch the browser in a desktop environment
            browser = p.chromium.launch()
            page = browser.new_page(
                viewport={
                    "width": iframe_width,
                    "height": iframe_height,
                },  # Set viewport size to desktop resolution
                user_agent=user_agent,
                # user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )

            # Open the desired URL
            page.goto(url)

            # Wait for the page to fully load, e.x. until there are no network connections for at least `500` ms
            page.wait_for_load_state("networkidle")

            # Get the HTML content after JavaScript execution
            html_content = page.content()

            # Close the browser
            browser.close()

        content = DomProcessor.convert_relative_to_absolute(
            base_url=url, html_content=html_content
        )
        content_type = "text/html"
        cache.set(
            CACHE_ADDRESS_FULLY_LOADED_BODY.format(url),
            content,
            timeout=60 * 5,
        )
        cache.set(
            CACHE_ADDRESS_CONTENT_TYPE.format(url),
            content_type,
            timeout=60 * 5,
        )

    return content, content_type


def fetch_response(url: str) -> tuple[str, str]:
    """
    Fetch the body of the given URL, aimed to be rendered inside an iframe in the client browser.
    """
    if content := cache.get(CACHE_ADDRESS_STATIC_BODY.format(url)):
        content_type = cache.get(CACHE_ADDRESS_CONTENT_TYPE.format(url))
    else:
        response = CrawlerService().fetch_response(url)
        content = DomProcessor.convert_relative_to_absolute(
            base_url=url, html_content=response.text
        )
        content_type = response.headers.get("Content-Type")
        cache.set(
            CACHE_ADDRESS_STATIC_BODY.format(url),
            content,
            timeout=60 * 5,
        )
        cache.set(
            CACHE_ADDRESS_CONTENT_TYPE.format(url),
            content_type,
            timeout=60 * 5,
        )
    return content, content_type
