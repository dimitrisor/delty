from django.db import models

from delty.models import PageSnapshot
from delty.models.base import BaseModel


class ElementSnapshot(BaseModel):
    page_snapshot = models.ForeignKey(PageSnapshot, on_delete=models.CASCADE)
    crawling_job = models.ForeignKey(
        "CrawlingJob",
        on_delete=models.CASCADE,
        related_name="element_snapshots",
        null=True,
        blank=True,
        default=None,
    )
    selector = models.TextField()
    # content = models.TextField()
    hash = models.CharField(max_length=64)
    # diff = models.TextField(null=True, default=None)
    version = models.IntegerField(default=1)
    content_path = models.TextField(default="")

    class Meta:
        unique_together = (
            ("page_snapshot", "selector", "hash"),
            ("page_snapshot", "selector", "version"),
        )
