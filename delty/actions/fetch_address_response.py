from delty.services.crawler import CrawlerService


class FetchAddressResponse:
    def execute(self, url: str) -> tuple[str, str]:
        return CrawlerService().fetch_response(url)


fetch_address_response = FetchAddressResponse()
