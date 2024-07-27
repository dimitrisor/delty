from dataclasses import dataclass

from django.contrib.auth.models import User

from delty.actions.common import fetch_response
from delty.services.crawler import CrawlerService


@dataclass
class CrawlingJobDto:
    id: str


class InitiateElementCrawling:
    crawler = CrawlerService()

    def execute(self, user: User, url: str, element_selector: str) -> CrawlingJobDto:
        content, _ = fetch_response(url)
        selected_element_content = self.crawler.get_selected_element_content(
            content, element_selector
        )
        crawling_job = self.crawler.create_crawling_job(
            user, url, element_selector, content, selected_element_content
        )
        return CrawlingJobDto(crawling_job.id)


initiate_element_crawling = InitiateElementCrawling()
