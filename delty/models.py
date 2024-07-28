import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models import DO_NOTHING


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class UrlAddress(BaseModel):
    url = models.URLField(unique=True, max_length=2083)


class PageSnapshot(BaseModel):
    address = models.ForeignKey(
        UrlAddress, on_delete=DO_NOTHING, related_name="page_snapshots"
    )
    hash = models.CharField(max_length=64)


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


class CrawlingJob(BaseModel):
    class Status(models.TextChoices):
        ACTIVE = "active"
        STOPPED = "stopped"
        FAILED = "failed"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url_address = models.ForeignKey(UrlAddress, on_delete=models.CASCADE)
    latest_element_snapshot = models.ForeignKey(
        ElementSnapshot, on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=255, choices=Status.choices, default=Status.ACTIVE
    )
    submitted_at = models.DateTimeField(auto_now=True)
