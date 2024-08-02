import logging
from dataclasses import dataclass

from django.contrib.auth.models import User

from delty.actions.common import fetch_response
from delty.exceptions import ServiceException
from delty.services.crawler import CrawlerService

logger = logging.getLogger(__name__)


@dataclass
class CrawlingJobDto:
    id: str


class InitiateElementCrawling:
    crawler_service = CrawlerService()

    def execute(self, actor: User, url: str, element_selector: str) -> CrawlingJobDto:
        try:
            content, _ = fetch_response(url)
            selected_element_content = (
                self.crawler_service.get_selected_element_content(
                    content, element_selector
                )
            )
            crawling_job = self.crawler_service.create_crawling_job(
                actor, url, element_selector, content, selected_element_content
            )
            logger.info(
                msg="Successfully initiated a crawling job.",
                extra={
                    "url": url,
                    "element_selector": element_selector,
                    "actor": actor.id,
                    "crawling_job": crawling_job.id,
                },
            )
            return CrawlingJobDto(crawling_job.id)
        except ServiceException as e:
            logger.error(
                msg="Failed to initiate a crawling job.",
                extra={
                    "url": url,
                    "element_selector": element_selector,
                    "actor": actor.id,
                },
            )
            raise e


initiate_element_crawling = InitiateElementCrawling()
