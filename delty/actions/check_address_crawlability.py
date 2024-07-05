from delty.services.crawler import CrawlerService


class CheckAddressCrawlability:
    def execute(self, url: str):
        CrawlerService().is_address_crawlable(url)


check_address_crawlability = CheckAddressCrawlability()
