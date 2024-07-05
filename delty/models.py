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
    url = models.URLField(unique=True)


class PageSnapshot(BaseModel):
    address = models.ForeignKey(UrlAddress, on_delete=DO_NOTHING)
    content = models.TextField()
    hash = models.CharField(max_length=64)


class SelectedElement(BaseModel):
    snapshot = models.ForeignKey(PageSnapshot, on_delete=models.CASCADE)
    content = models.TextField()
    hash = models.CharField(max_length=64, unique=True)
    selector = models.TextField()

    class Meta:
        unique_together = ("snapshot", "hash")


class CrawlingJob(BaseModel):
    class Status(models.TextChoices):
        ACTIVE = "active"
        STOPPED = "stopped"
        FAILED = "failed"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url_address = models.ForeignKey(UrlAddress, on_delete=models.CASCADE)
    selected_element = models.ForeignKey(SelectedElement, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=255, choices=Status.choices, default=Status.ACTIVE
    )
    submitted_at = models.DateTimeField(auto_now=True)
