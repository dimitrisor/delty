import logging

from django.contrib.auth.models import User

from delty.exceptions import ServiceException
from delty.services.crawler import CrawlerService

logger = logging.getLogger(__name__)


class CheckAddressCrawlability:
    def execute(self, actor: User, url: str):
        try:
            CrawlerService().is_address_crawlable(url)
        except ServiceException as e:
            logger.error(
                msg="Failed to check address crawlability.",
                extra={"url": url, "actor": actor.id},
            )
            raise e


check_address_crawlability = CheckAddressCrawlability()
