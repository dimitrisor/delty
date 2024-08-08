import difflib
from typing import Iterator

from bs4 import BeautifulSoup
from requests import Response, HTTPError

from delty.clients.web_client import WebClient
from delty.errors import (
    WebPageUnreachable,
    CssSelectorHtmlElementNotFound,
)
from delty.services.dom_processor import DomProcessor


class CrawlerService:
    def __init__(self):
        self.parser_cls = BeautifulSoup

    def fetch_response(self, url: str) -> Response:
        try:
            response = WebClient().get_response(url)
        except HTTPError:
            raise WebPageUnreachable(meta={"url": url})
        assert isinstance(response, Response)
        return response

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
        try:
            response_iterator = WebClient().get_response(url, True)
            if any(response_iterator):
                return True
        except HTTPError:
            pass
        raise WebPageUnreachable(meta={"url": url})

    def get_selected_element_content(self, page_html: str, css_selector: str) -> str:
        # create a new bs4 object from the html
        soup = self.parser_cls(page_html, "html.parser")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        css_selector = DomProcessor.escape_css_selector(css_selector=css_selector)

        if not (css_selector_html_element := soup.select(css_selector)):
            raise CssSelectorHtmlElementNotFound(
                meta={"css_selector": css_selector, "page_html": page_html}
            )

        # return the selected element
        return str(css_selector_html_element[0])

    def get_diff(self, base_html_lines: str, new_html_lines: str) -> Iterator[str]:
        base_lines = base_html_lines.splitlines()
        new_lines = new_html_lines.splitlines()
        return difflib.ndiff(base_lines, new_lines)
