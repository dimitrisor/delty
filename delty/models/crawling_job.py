from django.contrib.auth.models import User
from django.db import models

from delty.models import BaseModel, UrlAddress, ElementSnapshot


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
