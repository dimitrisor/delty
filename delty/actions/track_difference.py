import logging

import dramatiq
from django.contrib.auth import get_user_model

from delty.actions.common.fetch_response import fetch_response_fully_loaded
from delty.errors import ActorNotFound, CrawlingJobNotFound
from delty.exceptions import ServiceException
from delty.models import CrawlingJob, PageSnapshot, ElementSnapshot
from delty.services.crawler import CrawlerService
from delty.services.storage import StorageService
from delty.utils import compute_sha256

UserModel = get_user_model()
logger = logging.getLogger(__name__)


class TrackDifference:
    @staticmethod
    @dramatiq.actor(max_retries=10, actor_name="process_track_content_difference")
    def execute(actor_id: int, crawling_job_id: str):
        dramatiq.get_broker().logger.info("Message to be logged in the broker")

        if not (actor := UserModel.objects.get(id=actor_id)):
            raise ActorNotFound(meta={"actor_id": actor_id})

        if not (crawling_job := CrawlingJob.objects.get(id=crawling_job_id)):
            raise CrawlingJobNotFound(meta={"crawling_job_id": crawling_job_id})

        crawler = CrawlerService()
        s3_service = StorageService()
        try:
            url = crawling_job.url_address.url
            base_element_snapshot = crawling_job.latest_element_snapshot
            css_selector = base_element_snapshot.selector

            new_page_html, content_type = fetch_response_fully_loaded(
                url,
                crawling_job.iframe_width,
                crawling_job.iframe_height,
                crawling_job.user_agent,
            )

            new_element_content = crawler.get_selected_element_content(
                new_page_html, css_selector
            )
            new_element_content_hash = compute_sha256(new_element_content)
            assert new_element_content_hash is not None

            # Compare the base_element_content with the new_element_content
            # and store the difference in the database
            if base_element_snapshot.hash != new_element_content_hash:
                new_page_snapshot = PageSnapshot.objects.create(
                    address=crawling_job.url_address, hash=compute_sha256(new_page_html)
                )
                element_content_path = s3_service.upload_message(
                    new_element_content, new_element_content_hash
                )
                new_element_snapshot = ElementSnapshot.objects.create(
                    page_snapshot=new_page_snapshot,
                    crawling_job=crawling_job,
                    hash=new_element_content_hash,
                    selector=css_selector,
                    version=crawling_job.latest_element_snapshot.version + 1,
                    content_path=element_content_path,
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
            crawling_job.status = CrawlingJob.Status.FAILED
            crawling_job.save()
            logger.error(
                msg="Failed to track difference.",
                extra={
                    "url": url,
                    "actor": actor.id,
                    "crawling_job": crawling_job.id,
                },
            )
            raise e
