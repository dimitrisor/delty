import logging
import uuid
from dataclasses import dataclass

from django.contrib.auth.models import User
from django.db import transaction

from delty.actions.common import fetch_response
from delty.errors import CrawlingJobAlreadyExists
from delty.exceptions import ServiceException
from delty.models import CrawlingJob, UrlAddress, PageSnapshot, ElementSnapshot
from delty.services.crawler import CrawlerService
from delty.services.storage import StorageService
from delty.utils import compute_sha256

logger = logging.getLogger(__name__)


@dataclass
class CrawlingJobDto:
    id: str


class InitiateElementCrawling:
    crawler_service = CrawlerService()
    s3_service = StorageService()

    def execute(self, actor: User, url: str, element_selector: str) -> CrawlingJobDto:
        try:
            content_html, _ = fetch_response(url)
            selected_element_content = (
                self.crawler_service.get_selected_element_content(
                    content_html, element_selector
                )
            )

            with transaction.atomic():
                page_html_hash = compute_sha256(content_html)

                if CrawlingJob.objects.filter(
                    user=actor,
                    url_address__url=url,
                    selector=element_selector,
                    status=CrawlingJob.Status.ACTIVE,
                ).exists():
                    raise CrawlingJobAlreadyExists()

                address, _ = UrlAddress.objects.get_or_create(url=url)
                snapshot, _ = PageSnapshot.objects.get_or_create(
                    address=address,
                    hash=page_html_hash,
                )
                crawling_job_id = uuid.uuid4()
                selected_element, created = ElementSnapshot.objects.get_or_create(
                    page_snapshot=snapshot,
                    selector=element_selector,
                    hash=compute_sha256(selected_element_content),
                    defaults={
                        "content": selected_element_content,
                        "crawling_job_id": crawling_job_id,
                    },
                )
                if created:
                    element_content_path = self.s3_service.upload_message(
                        selected_element_content, selected_element.hash
                    )
                crawling_job = CrawlingJob.objects.create(
                    id=crawling_job_id,
                    user=actor,
                    url_address=address,
                    selector=element_selector,
                    latest_element_snapshot=selected_element,
                    status=CrawlingJob.Status.ACTIVE,
                )

                selected_element.content_path = element_content_path
                selected_element.crawling_job = crawling_job
                selected_element.save()

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
