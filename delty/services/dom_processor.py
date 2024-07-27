
from bs4 import BeautifulSoup


class DomProcessor:
    @staticmethod
    def convert_relative_to_absolute(base_url: str, html_content: str) -> str:
        soup = BeautifulSoup(html_content, "html.parser")

        # Convert relative paths in img tags
        for img in soup.find_all("img"):
            if img.attrs.get("src", "").startswith("/"):
                img.attrs["src"] = base_url + img.attrs["src"]
            if img.attrs.get("data-src", "").startswith("/"):
                img.attrs["data-src"] = base_url + img.attrs["data-src"]

        # Convert relative paths in link tags (for stylesheets)
        for link in soup.find_all("link", href=True):
            if link.attrs.get("href", "").startswith("/"):
                link.attrs["href"] = base_url + link.attrs["href"]

        # Convert relative paths in script tags
        for script in soup.find_all("script", src=True):
            if script.attrs.get("src", "").startswith("/"):
                script.attrs["src"] = base_url + script.attrs["src"]

        # You can add more conversions as needed for other tags

        return str(soup)

    @staticmethod
    def escape_css_selector(css_selector: str) -> str:
        # List of special characters to escape
        special_chars = r"@"
        # Escape each special character
        escaped_selector = "".join(
            ["\\" + char if char in special_chars else char for char in css_selector]
        )
        return escaped_selector
