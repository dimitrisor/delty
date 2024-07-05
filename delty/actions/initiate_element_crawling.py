from dataclasses import dataclass

from django.contrib.auth.models import User
from django.db import transaction

from delty.services.crawler import CrawlerService
from delty.models import UrlAddress, PageSnapshot, SelectedElement, CrawlingJob
from delty.utils import compute_sha256


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

        with transaction.atomic():
            address, _ = UrlAddress.objects.get_or_create(url=url)
            snapshot, _ = PageSnapshot.objects.get_or_create(
                address=address,
                hash=compute_sha256(page_html),
                defaults={"content": page_html},
            )
            selected_element = SelectedElement.objects.get_or_create(
                snapshot=snapshot,
                selector=element_selector,
                defaults={"content": selected_element_content},
            )
            crawling_job = CrawlingJob.objects.create(
                user=user,
                url_address=address,
                selected_element=selected_element,
                status=CrawlingJob.Status.ACTIVE,
            )

        return CrawlingJobDto(id=crawling_job.id)


initiate_element_crawling = InitiateElementCrawling()
