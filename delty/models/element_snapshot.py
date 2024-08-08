from django.db import models

from delty.models import BaseModel, PageSnapshot


class ElementSnapshot(BaseModel):
    page_snapshot = models.ForeignKey(PageSnapshot, on_delete=models.CASCADE)
    crawling_job = models.ForeignKey(
        "CrawlingJob", on_delete=models.CASCADE, related_name="element_snapshots"
    )
    selector = models.TextField()
    content = models.TextField()
    hash = models.CharField(max_length=64)
    diff = models.TextField(null=True, default=None)
    version = models.IntegerField(default=1)
    content_path = models.TextField(default="")

    class Meta:
        unique_together = (
            ("page_snapshot", "selector", "hash"),
            ("page_snapshot", "selector", "version"),
        )
