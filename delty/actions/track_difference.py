import logging

from bs4 import BeautifulSoup
from django.contrib.auth.models import User

from delty.actions.common.fetch_response import fetch_response_fully_loaded
from delty.exceptions import ServiceException
from delty.models import CrawlingJob, PageSnapshot, ElementSnapshot
from delty.services.crawler import CrawlerService
from delty.utils import compute_sha256

logger = logging.getLogger(__name__)


class TrackDifference:
    crawler = CrawlerService()

    def execute(self, actor: User, crawling_job: CrawlingJob):
        try:
            url = crawling_job.url_address.url
            base_element_snapshot = crawling_job.latest_element_snapshot
            base_element_snapshot_content = base_element_snapshot.content
            css_selector = base_element_snapshot.selector

            new_page_html, content_type = fetch_response_fully_loaded(
                url,
                crawling_job.iframe_width,
                crawling_job.iframe_height,
                crawling_job.user_agent,
            )

            new_element_content = self.crawler.get_selected_element_content(
                new_page_html, css_selector
            )
            new_element_content_hash = compute_sha256(new_element_content)

            # Compare the base_element_content with the new_element_content
            # and store the difference in the database
            if base_element_snapshot.hash != new_element_content_hash:
                BeautifulSoup(base_element_snapshot_content, "html.parser").prettify()
                BeautifulSoup(new_element_content, "html.parser").prettify()

                diff = self.crawler.get_diff(
                    str(base_element_snapshot_content), str(new_element_content)
                )
                new_page_snapshot = PageSnapshot.objects.create(
                    address=crawling_job.url_address, hash=compute_sha256(new_page_html)
                )
                new_element_snapshot = ElementSnapshot.objects.create(
                    page_snapshot=new_page_snapshot,
                    crawling_job=crawling_job,
                    content=new_element_content,
                    hash=new_element_content_hash,
                    selector=css_selector,
                    diff=diff,
                    version=crawling_job.latest_element_snapshot.version + 1,
                )
                crawling_job.latest_element_snapshot = new_element_snapshot
                crawling_job.save()
                logger.info(
                    msg="Difference in htmls found.",
                    extra={
                        "url": url,
                        "actor": actor.id,
                        "crawling_job": crawling_job.id,
                    },
                )
            logger.info(
                msg="Successfully run difference tracking.",
                extra={
                    "url": url,
                    "actor": actor.id,
                    "crawling_job": crawling_job.id,
                },
            )
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


track_difference = TrackDifference()
