import logging

from django.contrib.auth.models import User

from delty.actions.common import fetch_response
from delty.exceptions import ServiceException
from delty.models import CrawlingJob
from delty.services.crawler import CrawlerService

logger = logging.getLogger(__name__)


class TrackDifference:
    crawler = CrawlerService()

    def execute(self, actor: User, crawling_job: CrawlingJob):
        try:
            url = crawling_job.url_address.url
            selected_element = crawling_job.selected_element
            base_selected_element_content = selected_element.content

            new_page_html, content_type = fetch_response(url)
            new_selected_element_content = self.crawler.get_selected_element_content(
                new_page_html, selected_element.selector
            )

            # Compare the base_selected_element_content with the new_selected_element_content
            # and store the difference in the database
            diff = self.crawler.get_diff(
                base_selected_element_content, new_selected_element_content
            )
            if diff:
                self.crawler.create_crawling_job(
                    actor,
                    url,
                    selected_element.selector,
                    new_page_html,
                    new_selected_element_content,
                )
            pass
        except ServiceException as e:
            logger.error(
                msg="Failed to track difference.",
                extra={
                    "url": url,
                    "actor": actor.id,
                    "crawling_job": crawling_job.id,
                },
            )
            raise e
