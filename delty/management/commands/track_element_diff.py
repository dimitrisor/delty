import logging

from django.core.management.base import BaseCommand

from delty.tasks import TrackDifference
from delty.models import CrawlingJob

# dramatiq.set_broker("redis://localhost:6379")
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "This runs the difference tracking process for all active crawling jobs."

    def handle(self, *args, **kwargs):
        for crawling_job in CrawlingJob.objects.filter(
            status=CrawlingJob.Status.ACTIVE
        ):
            TrackDifference.execute.send(crawling_job.user.id, str(crawling_job.id))

        logger.info(msg="All active crawling jobs have successfully ran.")
