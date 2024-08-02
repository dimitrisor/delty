from django.db import models

from delty.models import BaseModel, PageSnapshot


class ElementSnapshot(BaseModel):
    page_snapshot = models.ForeignKey(PageSnapshot, on_delete=models.CASCADE)
    selector = models.TextField()
    content = models.TextField()
    hash = models.CharField(max_length=64)
    diff = models.TextField(null=True, default=None)
    version = models.IntegerField(default=1)

    class Meta:
        unique_together = (
            ("page_snapshot", "selector", "hash"),
            ("page_snapshot", "selector", "version"),
        )
