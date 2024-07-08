from dataclasses import dataclass

from django.contrib.auth.models import User

from delty.services.crawler import CrawlerService


@dataclass
class CrawlingJobDto:
    id: str


class InitiateElementCrawling:
    crawler = CrawlerService()

    def execute(self, user: User, url: str, element_selector: str) -> CrawlingJobDto:
        page_html, content_type = self.crawler.fetch_response(url)
        selected_element_content = self.crawler.get_selected_element_content(
            page_html, element_selector
        )
        crawling_job = self.crawler.create_crawling_job(
            user, url, element_selector, page_html, selected_element_content
        )
        return CrawlingJobDto(crawling_job.id)


initiate_element_crawling = InitiateElementCrawling()
