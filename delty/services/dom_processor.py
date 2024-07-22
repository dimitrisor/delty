import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup


class DomProcessor:
    @staticmethod
    def replace_relative_links(base_url, html_content):
        # Define a regex pattern to find relative links in src and href attributes
        pattern = re.compile(
            r'(<\s*(img|script|a|link)\s+[^>]*(src|href)\s*=\s*["\'])(?!http|https|ftp|//)([^"\']+)["\']',
            re.IGNORECASE,
        )

        # Function to replace each match with the absolute URL
        def replace_match(match):
            # Extract the full match and the relative URL
            match.group(0)
            relative_url = match.group(4)
            absolute_url = urljoin(base_url, relative_url)

            # Replace the relative URL with the absolute URL
            new_link = match.group(1) + absolute_url + '"'
            return new_link

        # Use re.sub to replace all relative links with absolute links
        updated_html = re.sub(pattern, replace_match, html_content)

        return updated_html

    @staticmethod
    def convert_relative_to_absolute(base_url, html_content):
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
    def escape_css_selector(css_selector):
        # List of special characters to escape
        special_chars = r"@"
        # Escape each special character
        escaped_selector = "".join(
            ["\\" + char if char in special_chars else char for char in css_selector]
        )
        return escaped_selector
