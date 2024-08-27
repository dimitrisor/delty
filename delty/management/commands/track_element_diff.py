import logging

from django.core.management.base import BaseCommand

from delty.actions.track_difference import track_difference
from delty.models import CrawlingJob

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "This runs the difference tracking process for all active crawling jobs."

    def handle(self, *args, **kwargs):
        for crawling_job in CrawlingJob.objects.filter(
            status=CrawlingJob.Status.ACTIVE
        ):
            track_difference.execute(crawling_job.user, crawling_job)

        logger.info(msg="All active crawling jobs have successfully ran.")
