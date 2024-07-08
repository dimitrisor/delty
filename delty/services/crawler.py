import difflib
from typing import Iterator

from bs4 import BeautifulSoup
from django.core.cache import cache
from django.db import transaction
from requests import Response

from delty.clients.web_client import WebClient
from delty.constants import CACHE_ADDRESS_TEXT, CACHE_ADDRESS_CONTENT_TYPE
from delty.errors import WebPageUnreachable
from delty.models import SelectedElement, UrlAddress, PageSnapshot, CrawlingJob
from delty.utils import compute_sha256


class CrawlerService:
    def __init__(self):
        self.parser_cls = BeautifulSoup

    def fetch_response(
        self, url: str, check_crawlability: bool = False
    ) -> tuple[str, str]:
        if text := cache.get(CACHE_ADDRESS_TEXT.format(url)):
            content_type = cache.get(CACHE_ADDRESS_CONTENT_TYPE.format(url))
        else:
            response = WebClient().get_response(url, check_crawlability)
            assert isinstance(response, Response)
            text = response.text
            content_type = response.headers.get("Content-Type")
            cache.set(
                CACHE_ADDRESS_TEXT.format(url),
                text,
                timeout=60 * 5,
            )
            cache.set(
                CACHE_ADDRESS_CONTENT_TYPE.format(url),
                content_type,
                timeout=60 * 5,
            )

        return text, content_type

    def is_address_crawlable(self, url: str) -> bool:
        """
        Checks if the given URL is crawlable.

        This method sends a GET request to the URL and checks if the response is iterable.
        If all elements in the response iterator are False, it raises a WebPageUnreachable exception.
        If the URL is crawlable, it returns True.

        Args:
            url (str): The URL to be checked for crawlability.

        Returns:
            bool: True if the URL is crawlable, otherwise raises an exception.

        Raises:
            WebPageUnreachable: If all elements in the response iterator are False.
        """
        response_iterator = WebClient().get_response(url, True)
        if all(False for _ in response_iterator):
            raise WebPageUnreachable(meta={"url": url})
        return True

    def get_selected_element_content(self, page_html: str, css_selector: str) -> str:
        # create a new bs4 object from the html
        soup = self.parser_cls(page_html, "html.parser")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        # return the selected element
        return str(soup.select(css_selector)[0])

    def get_diff(self, base_html_lines: str, new_html_lines: str) -> Iterator[str]:
        base_lines = base_html_lines.splitlines()
        new_lines = new_html_lines.splitlines()
        return difflib.ndiff(base_lines, new_lines)

    def create_crawling_job(
        self, user, url, element_selector, page_html, selected_element_content
    ):
        with transaction.atomic():
            address, _ = UrlAddress.objects.get_or_create(url=url)
            snapshot, _ = PageSnapshot.objects.get_or_create(
                address=address,
                hash=compute_sha256(page_html),
                defaults={"content": page_html},
            )
            selected_element, _ = SelectedElement.objects.get_or_create(
                snapshot=snapshot,
                selector=element_selector,
                hash=compute_sha256(selected_element_content),
                defaults={"content": selected_element_content},
            )
            crawling_job = CrawlingJob.objects.create(
                user=user,
                url_address=address,
                selected_element=selected_element,
                status=CrawlingJob.Status.ACTIVE,
            )

        return crawling_job
