from django.contrib.auth.models import User
from django.db import models

from delty.models import UrlAddress, ElementSnapshot
from delty.models.base import BaseModel


class CrawlingJob(BaseModel):
    class Status(models.TextChoices):
        ACTIVE = "active"
        STOPPED = "stopped"
        FAILED = "failed"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url_address = models.ForeignKey(UrlAddress, on_delete=models.CASCADE)
    latest_element_snapshot = models.ForeignKey(
        ElementSnapshot, on_delete=models.DO_NOTHING, null=True
    )
    selector = models.TextField()
    iframe_width = models.IntegerField()
    iframe_height = models.IntegerField()
    user_agent = models.CharField(max_length=255)
    status = models.CharField(
        max_length=255, choices=Status.choices, default=Status.ACTIVE
    )
    submitted_at = models.DateTimeField(auto_now=True)
